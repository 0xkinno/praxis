import unittest
from datetime import datetime, timezone
from praxis.models import TrustScore, DimensionScore, TrustGrade, TrustTier
from praxis.scoring.propagation import PropagationEngine

class TestTrustPropagation(unittest.TestCase):
    
    def test_propagation_cascade(self):
        # Setup mock trust scores
        # Node A: composite_score = 40 (untrusted)
        # Node B: composite_score = 80 (downstream of A, hop 1)
        # Node C: composite_score = 90 (downstream of B, hop 2)
        # Node D: composite_score = 85 (independent)
        
        assessed_time = datetime.now(timezone.utc)
        dummy_dim = DimensionScore(name="dummy", score=100.0, evidence=[], weight=0.2)
        dims = {d: dummy_dim for d in ["provenance", "integrity", "stability", "lineage", "adoption"]}
        
        trust_scores = {
            "urn:li:dataset:A": TrustScore(
                urn="urn:li:dataset:A", name="A", platform="hive",
                composite_score=40.0, grade=TrustGrade.F, tier=TrustTier.UNTRUSTED,
                dimensions=dims, assessed_at=assessed_time, evidence_summary=""
            ),
            "urn:li:dataset:B": TrustScore(
                urn="urn:li:dataset:B", name="B", platform="hive",
                composite_score=80.0, grade=TrustGrade.B_PLUS, tier=TrustTier.TRUSTED,
                dimensions=dims, assessed_at=assessed_time, evidence_summary=""
            ),
            "urn:li:dataset:C": TrustScore(
                urn="urn:li:dataset:C", name="C", platform="hive",
                composite_score=90.0, grade=TrustGrade.A, tier=TrustTier.TRUSTED,
                dimensions=dims, assessed_at=assessed_time, evidence_summary=""
            ),
            "urn:li:dataset:D": TrustScore(
                urn="urn:li:dataset:D", name="D", platform="hive",
                composite_score=85.0, grade=TrustGrade.A_MINUS, tier=TrustTier.TRUSTED,
                dimensions=dims, assessed_at=assessed_time, evidence_summary=""
            ),
        }
        
        lineage_graph = {
            "urn:li:dataset:A": ["urn:li:dataset:B"],
            "urn:li:dataset:B": ["urn:li:dataset:C"],
            # D is isolated
        }
        
        engine = PropagationEngine(factor=0.3, decay=0.7)
        res = engine.propagate(trust_scores, lineage_graph, threshold=55.0)
        
        self.assertEqual(res["affected_count"], 2)
        
        affected = {a["urn"]: a for a in res["affected_assets"]}
        self.assertIn("urn:li:dataset:B", affected)
        self.assertIn("urn:li:dataset:C", affected)
        self.assertNotIn("urn:li:dataset:D", affected)
        
        # Calculate expected penalties:
        # A is source of untrust (score = 40.0). Max potential penalty = (100 - 40) = 60.0.
        # factor = 0.3. Raw penalty = 60 * 0.3 = 18.0.
        # Hop 1 (B): decayed = 18 * (0.7 ** 0) = 18.0. Propagated score = 80 - 18 = 62.0.
        # Hop 2 (C): decayed = 18 * (0.7 ** 1) = 12.6. Propagated score = 90 - 12.6 = 77.4.
        
        self.assertAlmostEqual(affected["urn:li:dataset:B"]["penalty"], 18.0, places=1)
        self.assertAlmostEqual(affected["urn:li:dataset:B"]["propagated_score"], 62.0, places=1)
        
        self.assertAlmostEqual(affected["urn:li:dataset:C"]["penalty"], 12.6, places=1)
        self.assertAlmostEqual(affected["urn:li:dataset:C"]["propagated_score"], 77.4, places=1)
        
        # Check paths
        paths = res["paths"]
        self.assertEqual(len(paths), 2)
        self.assertEqual(paths[0]["source"], "urn:li:dataset:A")
        self.assertEqual(paths[0]["target"], "urn:li:dataset:B")
        self.assertEqual(paths[0]["penalty"], 18.0)
        self.assertEqual(paths[0]["hop"], 1)
        
        self.assertEqual(paths[1]["source"], "urn:li:dataset:B")
        self.assertEqual(paths[1]["target"], "urn:li:dataset:C")
        self.assertEqual(paths[1]["penalty"], 12.6)
        self.assertEqual(paths[1]["hop"], 2)

if __name__ == "__main__":
    unittest.main()
