import unittest
from unittest.mock import MagicMock
from praxis.models import MLVerdict
from praxis.ml.gate import PraxisMLGate

class TestMLGate(unittest.TestCase):
    
    def setUp(self):
        self.mock_client = MagicMock()
        self.gate = PraxisMLGate(self.mock_client)
        
    def test_safe_to_train(self):
        # Setup: Target dataset score is 80 (Trusted), upstream is 70 (Trusted)
        target_urn = "urn:li:dataset:target"
        upstream_urn = "urn:li:dataset:upstream"
        
        # Mock get_entity_detail for target
        self.mock_client.get_entity_detail.side_effect = lambda urn: {
            "urn": urn,
            "name": urn.split(":")[-1],
            "platform": {"name": "hive"},
            # To get score = 80 (Provenance):
            # ownership: ok, desc: ok, schema: ok, glossary: ok, domain: ok = score 100
            # Wait, let's just make it completely perfect to get 100
            "ownership": {"owners": [{"owner": "u1"}, {"owner": "u2"}]},
            "properties": {"description": "A very long description that is at least fifty characters long."},
            "schemaMetadata": {
                "fields": [
                    {"fieldPath": "id", "nullable": False, "description": "PK"}
                ],
                "primaryKeys": ["id"]
            },
            "glossaryTerms": {"terms": [{"term": "t"}]},
            "domain": {"domain": {"properties": {"name": "Core"}}},
            # Let's set integrity dimensions to pass (100)
            "assertions": {"assertions": [{"runEvents": {"runEvents": [{"result": {"type": "SUCCESS"}}]}}]},
            "health": [{"status": "PASS"}],
            "deprecation": {"deprecated": False},
            # usageStats: (100)
            "usageStats": {"aggregations": {"totalSqlQueries": 100, "uniqueUserCount": 10}}
        }
        
        # Upstream lineage mocks
        self.mock_client.get_upstream_lineage.side_effect = lambda urn: (
            [{"entity": {"urn": upstream_urn, "type": "DATASET"}}] if urn == target_urn else []
        )
        self.mock_client.get_downstream_lineage.side_effect = lambda urn: (
            [
                {"entity": {"urn": "urn:li:dataset:down1", "type": "DATASET"}},
                {"entity": {"urn": "urn:li:dashboard:down2", "type": "DASHBOARD"}}
            ] if urn in (target_urn, upstream_urn) else []
        )
        
        res = self.gate.check_training_data([target_urn])
        
        self.assertEqual(res.verdict, MLVerdict.SAFE_TO_TRAIN)
        self.assertEqual(len(res.sources), 1)
        self.assertEqual(res.sources[0]["score"], 100.0)
        self.assertEqual(len(res.upstream_risks), 0)
        
    def test_block_training_target_low(self):
        # Target dataset score is low (< 55)
        target_urn = "urn:li:dataset:target"
        
        self.mock_client.get_entity_detail.return_value = {
            "urn": target_urn,
            "name": "target",
            "ownership": {"owners": []},  # -30
            "properties": {"description": ""},  # -25
            "schemaMetadata": {"fields": []},  # -25
            "glossaryTerms": {"terms": []},  # -10
            "domain": None,  # -10
            # score is 0.0
        }
        self.mock_client.get_upstream_lineage.return_value = []
        self.mock_client.get_downstream_lineage.return_value = []
        
        res = self.gate.check_training_data([target_urn])
        
        self.assertEqual(res.verdict, MLVerdict.BLOCK_TRAINING)
        self.assertEqual(res.sources[0]["score"], 33.8) # Composite score for poor asset = 33.8
        self.assertIn("direct sources are untrusted", res.summary)

    def test_block_training_upstream_low(self):
        # Target is perfect, but upstream is low (< 40)
        target_urn = "urn:li:dataset:target"
        upstream_urn = "urn:li:dataset:upstream"
        
        def mock_get_entity_detail(urn):
            if urn == target_urn:
                return {
                    "urn": target_urn, "name": "target", "platform": {"name": "hive"},
                    "ownership": {"owners": [{"owner": "u1"}, {"owner": "u2"}]},
                    "properties": {"description": "A very long description that is at least fifty characters long."},
                    "schemaMetadata": {"fields": [{"fieldPath": "id", "nullable": False, "description": "PK"}], "primaryKeys": ["id"]},
                    "glossaryTerms": {"terms": [{"term": "t"}]},
                    "domain": {"domain": {"properties": {"name": "Core"}}},
                    "assertions": {"assertions": [{"runEvents": {"runEvents": [{"result": {"type": "SUCCESS"}}]}}]},
                    "health": [{"status": "PASS"}], "deprecation": {"deprecated": False},
                    "usageStats": {"aggregations": {"totalSqlQueries": 100, "uniqueUserCount": 10}}
                }
            else: # upstream is completely poor
                return {
                    "urn": upstream_urn, "name": "upstream", "platform": {"name": "hive"},
                    "ownership": {"owners": []}, "properties": {"description": ""},
                    "schemaMetadata": {"fields": []}, "glossaryTerms": {"terms": []}, "domain": None
                }
                
        self.mock_client.get_entity_detail.side_effect = mock_get_entity_detail
        self.mock_client.get_upstream_lineage.side_effect = lambda urn: (
            [{"entity": {"urn": upstream_urn, "type": "DATASET"}}] if urn == target_urn else []
        )
        self.mock_client.get_downstream_lineage.return_value = []
        
        res = self.gate.check_training_data([target_urn])
        
        self.assertEqual(res.verdict, MLVerdict.BLOCK_TRAINING)
        self.assertEqual(len(res.upstream_risks), 1)
        self.assertEqual(res.upstream_risks[0]["urn"], upstream_urn)
        self.assertEqual(res.upstream_risks[0]["score"], 33.8) # < 40 block
        
    def test_caution_training_upstream(self):
        # Target is perfect, but upstream is slightly degraded (between 40 and 59)
        target_urn = "urn:li:dataset:target"
        upstream_urn = "urn:li:dataset:upstream"
        
        def mock_get_entity_detail(urn):
            if urn == target_urn:
                return {
                    "urn": target_urn, "name": "target", "platform": {"name": "hive"},
                    "ownership": {"owners": [{"owner": "u1"}, {"owner": "u2"}]},
                    "properties": {"description": "A very long description that is at least fifty characters long."},
                    "schemaMetadata": {"fields": [{"fieldPath": "id", "nullable": False, "description": "PK"}], "primaryKeys": ["id"]},
                    "glossaryTerms": {"terms": [{"term": "t"}]},
                    "domain": {"domain": {"properties": {"name": "Core"}}},
                    "assertions": {"assertions": [{"runEvents": {"runEvents": [{"result": {"type": "SUCCESS"}}]}}]},
                    "health": [{"status": "PASS"}], "deprecation": {"deprecated": False},
                    "usageStats": {"aggregations": {"totalSqlQueries": 100, "uniqueUserCount": 10}}
                }
            else: # upstream is medium
                return {
                    "urn": upstream_urn, "name": "upstream", "platform": {"name": "hive"},
                    # score will be ~56.2 (Provenance = 70 (single owner: -10, description ok, fields ok, domain/glossary missing = -20))
                    # Let's mock a specific medium score:
                    "ownership": {"owners": [{"owner": "u1"}]}, # -10
                    "properties": {"description": "A very long description that is at least fifty characters long."},
                    "schemaMetadata": {"fields": [{"fieldPath": "id", "nullable": False, "description": "PK"}], "primaryKeys": ["id"]},
                    "glossaryTerms": {"terms": []}, # -10
                    "domain": None, # -10
                    # Provenance score = 70
                    # Let's set integrity assertions = missing (-40), health = missing (-10), deprecation = 0 -> score = 50
                    # Let's set stability: fields ok, pk ok -> score = 100
                    # Lineage isolated -> score = 30
                    # Adoption missing -> score = 50
                    # Composite score = 70 * 0.25 + 50 * 0.30 + 100 * 0.15 + 30 * 0.15 + 50 * 0.15
                    # = 17.5 + 15 + 15 + 4.5 + 7.5 = 59.5 (which is within [40, 60))
                }
                
        self.mock_client.get_entity_detail.side_effect = mock_get_entity_detail
        self.mock_client.get_upstream_lineage.side_effect = lambda urn: (
            [{"entity": {"urn": upstream_urn, "type": "DATASET"}}] if urn == target_urn else []
        )
        self.mock_client.get_downstream_lineage.return_value = []
        
        res = self.gate.check_training_data([target_urn])
        
        self.assertEqual(res.verdict, MLVerdict.CAUTION)
        self.assertEqual(len(res.upstream_risks), 1)
        self.assertEqual(res.upstream_risks[0]["score"], 59.5)

if __name__ == "__main__":
    unittest.main()
