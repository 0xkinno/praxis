import unittest
from datetime import datetime
from praxis.models import TrustGrade, TrustTier
from praxis.scoring.provenance import score_provenance
from praxis.scoring.integrity import score_integrity
from praxis.scoring.stability import score_stability
from praxis.scoring.lineage import score_lineage
from praxis.scoring.adoption import score_adoption
from praxis.scoring.engine import compute_trust_score

class TestScoringDimensions(unittest.TestCase):
    
    def test_score_provenance(self):
        # Perfect asset
        entity = {
            "ownership": {"owners": [{"owner": "user1"}, {"owner": "user2"}]},
            "editableProperties": {"description": "This is a detailed description of the dataset that is longer than 50 characters."},
            "schemaMetadata": {
                "fields": [
                    {"fieldPath": "id", "description": "Identifier"},
                    {"fieldPath": "name", "description": "Name"}
                ]
            },
            "glossaryTerms": {"terms": [{"term": "term1"}]},
            "domain": {"domain": {"properties": {"name": "Finance"}}}
        }
        res = score_provenance(entity)
        self.assertEqual(res.score, 100.0)
        
        # Missing owners and descriptions
        entity_poor = {
            "ownership": {"owners": []},
            "properties": {"description": ""},
            "schemaMetadata": {"fields": []},
            "glossaryTerms": {"terms": []},
            "domain": None
        }
        res_poor = score_provenance(entity_poor)
        # Deductions: owners (-30), desc (-25), fields (-25), terms (-10), domain (-10) = -100
        self.assertEqual(res_poor.score, 0.0)
        
    def test_score_integrity(self):
        # Perfect asset: assertions pass rate 100%, health checks pass, not deprecated
        entity = {
            "assertions": {
                "assertions": [
                    {
                        "runEvents": {
                            "runEvents": [
                                {"result": {"type": "SUCCESS"}}
                            ]
                        }
                    }
                ]
            },
            "health": [{"status": "PASS"}],
            "deprecation": {"deprecated": False}
        }
        res = score_integrity(entity)
        self.assertEqual(res.score, 100.0)
        
        # Deprecated and failing assertions
        entity_bad = {
            "assertions": {
                "assertions": [
                    {
                        "runEvents": {
                            "runEvents": [
                                {"result": {"type": "FAILURE"}}
                            ]
                        }
                    }
                ]
            },
            "health": [{"status": "FAIL"}],
            "deprecation": {"deprecated": True, "note": "Outdated"}
        }
        res_bad = score_integrity(entity_bad)
        # Deductions:
        # Assertions exist (evidence of definition = no -40), but pass rate 0% (<50%: -30), failing count = 1 (-3),
        # Health issues = 1 (-10), Deprecated (-20) = -63 total deductions.
        # Score = 100 - 63 = 37.0
        self.assertEqual(res_bad.score, 37.0)

    def test_score_stability(self):
        # Perfect stability
        entity = {
            "schemaMetadata": {
                "fields": [
                    {"fieldPath": "id", "nullable": False, "description": "PK"},
                    {"fieldPath": "val", "nullable": True, "description": "documented val"}
                ],
                "primaryKeys": ["id"]
            }
        }
        res = score_stability(entity)
        self.assertEqual(res.score, 100.0)
        
        # Poor stability: no primary keys, high nullable undocumented fields
        entity_poor = {
            "schemaMetadata": {
                "fields": [
                    {"fieldPath": "id", "nullable": True},  # Undocumented and nullable
                    {"fieldPath": "val", "nullable": True}  # Undocumented and nullable
                ],
                "primaryKeys": []
            }
        }
        res_poor = score_stability(entity_poor)
        # Deductions: PK missing (-15), >50% nullable undocumented (-15) = -30
        self.assertEqual(res_poor.score, 70.0)

    def test_score_lineage(self):
        # Connected both ways, multiple consumers of different types
        entity = {}
        lineage_data = {
            "upstream": [{"entity": {"urn": "up1"}}],
            "downstream": [
                {"entity": {"urn": "down1", "type": "DATASET"}},
                {"entity": {"urn": "down2", "type": "DASHBOARD"}}
            ]
        }
        res = score_lineage(entity, lineage_data)
        self.assertEqual(res.score, 100.0)
        
        # Isolated asset
        lineage_isolated = {
            "upstream": [],
            "downstream": []
        }
        res_isolated = score_lineage(entity, lineage_isolated)
        # Deductions: upstream missing (-30), downstream missing (-30), isolation additional (-10) = -70
        self.assertEqual(res_isolated.score, 30.0)

    def test_score_adoption(self):
        # Active asset
        entity = {
            "usageStats": {
                "aggregations": {
                    "totalSqlQueries": 100,
                    "uniqueUserCount": 10
                }
            }
        }
        res = score_adoption(entity)
        self.assertEqual(res.score, 100.0)
        
        # Missing stats fallback
        entity_missing = {}
        res_missing = score_adoption(entity_missing)
        self.assertEqual(res_missing.score, 50.0)

    def test_composite_score(self):
        entity = {
            "ownership": {"owners": []},  # -30 = score 70 (Provenance)
            "assertions": {"assertions": []}, # -40 = score 60 (Integrity), wait health check missing will be -10, so 50
            "schemaMetadata": {"fields": []}, # -40 = score 60, wait PK missing will be -15, so 45 (Stability)
        }
        lineage = {"upstream": [], "downstream": []} # score 30 (Lineage)
        # Adoption fallback = 50 (Adoption)
        # Wait, let's trace Provenance score:
        # owners: missing (-30)
        # description: missing (-25)
        # fields: missing (-25)
        # terms: missing (-10)
        # domain: missing (-10)
        # Provenance Score = 0
        
        # Integrity score:
        # assertions: missing (-40)
        # health: missing (-10)
        # deprecation: not deprecated (0)
        # Integrity Score = 50
        
        # Stability score:
        # fields: missing (-40)
        # PK: missing (-15)
        # Stability Score = 45
        
        # Lineage Score = 30
        # Adoption Score = 50
        
        # Composite score:
        # 0 * 0.25 + 50 * 0.30 + 45 * 0.15 + 30 * 0.15 + 50 * 0.15
        # = 0 + 15 + 6.75 + 4.5 + 7.5 = 33.75
        ts = compute_trust_score(entity, lineage)
        self.assertAlmostEqual(ts.composite_score, 33.8, places=1)
        self.assertEqual(ts.grade, TrustGrade.F)
        self.assertEqual(ts.tier, TrustTier.UNTRUSTED)

if __name__ == "__main__":
    unittest.main()
