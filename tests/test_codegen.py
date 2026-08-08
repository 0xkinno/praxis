import unittest
from datetime import datetime, timezone
from praxis.models import TrustScore, DimensionScore, TrustGrade, TrustTier
from praxis.codegen.generator import generate_artifacts

class TestCodegen(unittest.TestCase):
    
    def test_generate_artifacts(self):
        assessed_time = datetime.now(timezone.utc)
        
        # Provenance: 80, Integrity: 50 (should trigger freshness), Stability: 70, Lineage: 80, Adoption: 80
        dummy_dim = DimensionScore(name="dummy", score=80.0, evidence=["Evidence"], weight=0.25)
        integrity_dim = DimensionScore(name="integrity", score=50.0, evidence=["Low integrity"], weight=0.30)
        
        dims = {
            "provenance": dummy_dim,
            "integrity": integrity_dim,
            "stability": dummy_dim,
            "lineage": dummy_dim,
            "adoption": dummy_dim
        }
        
        trust_score = TrustScore(
            urn="urn:li:dataset:(urn:li:dataPlatform:hive,my_dataset,PROD)",
            name="my_dataset",
            platform="hive",
            composite_score=72.0,
            grade=TrustGrade.C_PLUS,
            tier=TrustTier.REVIEW,
            dimensions=dims,
            assessed_at=assessed_time,
            evidence_summary="Assessed low integrity"
        )
        
        entity_data = {
            "urn": "urn:li:dataset:(urn:li:dataPlatform:hive,my_dataset,PROD)",
            "name": "my_dataset",
            "platform": {"name": "hive"},
            "properties": {
                "qualifiedName": "hive.my_dataset",
                "description": "This is my dataset description."
            },
            "schemaMetadata": {
                "fields": [
                    {"fieldPath": "id", "type": "NUMBER", "nativeDataType": "INT", "nullable": False, "description": "Primary key"},
                    {"fieldPath": "updated_at", "type": "TIME", "nativeDataType": "TIMESTAMP", "nullable": True, "description": "Last updated timestamp"},
                    {"fieldPath": "val", "type": "STRING", "nativeDataType": "VARCHAR", "nullable": True}
                ],
                "primaryKeys": ["id"]
            },
            "ownership": {
                "owners": [
                    {"owner": {"username": "admin", "editableProperties": {"displayName": "System Admin"}}}
                ]
            },
            "domain": {
                "domain": {
                    "properties": {"name": "Core"}
                }
            }
        }
        
        artifacts = generate_artifacts(trust_score, entity_data)
        
        # Verify 5 files are generated: dbt_test, assertion, contract, documentation, freshness
        self.assertEqual(len(artifacts), 5)
        
        types = {a.artifact_type: a for a in artifacts}
        self.assertIn("dbt_test", types)
        self.assertIn("assertion", types)
        self.assertIn("contract", types)
        self.assertIn("documentation", types)
        self.assertIn("freshness", types)
        
        # Verify dbt_test grounding
        dbt_test = types["dbt_test"]
        self.assertEqual(dbt_test.filename, "schema_test.yml")
        self.assertIn("my_dataset", dbt_test.content)
        self.assertIn("updated_at", dbt_test.content)
        self.assertIn("tests:\n          - unique\n          - not_null", dbt_test.content) # id column tests
        
        # Verify assertion content
        assertion = types["assertion"]
        self.assertIn("urn:li:dataset:(urn:li:dataPlatform:hive,my_dataset,PROD)", assertion.content)
        self.assertIn("id must not be null", assertion.content) # id is non-nullable
        
        # Verify contract content
        contract = types["contract"]
        self.assertIn("my_dataset_contract", contract.content)
        self.assertIn("- field: \"id\"", contract.content)
        
        # Verify documentation
        doc = types["documentation"]
        self.assertIn("System Admin", doc.content)
        self.assertIn("Core", doc.content)
        self.assertIn("C+", doc.content)
        
        # Verify freshness
        freshness = types["freshness"]
        self.assertIn("loaded_at_field: updated_at", freshness.content) # guessed updated_at field

if __name__ == "__main__":
    unittest.main()
