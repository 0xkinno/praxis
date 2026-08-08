import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from praxis.models import TrustScore, DimensionScore, TrustGrade, TrustTier, GeneratedArtifact
from praxis.github.pr_creator import PraxisPRCreator
from github.GithubException import GithubException

class TestPRCreator(unittest.TestCase):
    
    def test_remediation_pr_skipped(self):
        # Missing token/repo
        creator = PraxisPRCreator("", "")
        res = creator.create_remediation_pr("run_123", [], [])
        self.assertEqual(res["status"], "skipped")
        self.assertIn("missing token or repo", res["reason"])
        
    @patch("praxis.github.pr_creator.Github")
    def test_remediation_pr_success(self, mock_github_class):
        # Mock PyGithub interactions
        mock_github = MagicMock()
        mock_github_class.return_value = mock_github
        
        mock_repo = MagicMock()
        mock_github.get_repo.return_value = mock_repo
        
        mock_repo.default_branch = "main"
        
        mock_branch = MagicMock()
        mock_branch.commit.sha = "abcdef123456"
        mock_repo.get_branch.return_value = mock_branch
        
        mock_pr = MagicMock()
        mock_pr.html_url = "https://github.com/test/repo/pull/1"
        mock_pr.number = 1
        mock_repo.create_pull.return_value = mock_pr
        
        # When get_contents throws 404, file is created
        mock_repo.get_contents.side_effect = GithubException(404, "Not Found", {})
        
        assessed_time = datetime.now(timezone.utc)
        dummy_dim = DimensionScore(name="dummy", score=80.0, evidence=["Evidence"], weight=0.2)
        dims = {d: dummy_dim for d in ["provenance", "integrity", "stability", "lineage", "adoption"]}
        
        trust_scores = [
            TrustScore(
                urn="urn:li:dataset:my_asset",
                name="my_asset",
                platform="hive",
                composite_score=60.0,
                grade=TrustGrade.C,
                tier=TrustTier.REVIEW,
                dimensions=dims,
                assessed_at=assessed_time,
                evidence_summary="summary"
            )
        ]
        
        generated_artifacts = [
            GeneratedArtifact(
                artifact_type="dbt_test",
                target_urn="urn:li:dataset:my_asset",
                filename="schema_test.yml",
                content="dbt test content",
                generated_at=assessed_time,
                grounding_evidence=[]
            )
        ]
        
        creator = PraxisPRCreator("my_token", "test/repo")
        res = creator.create_remediation_pr("run_12345678", trust_scores, generated_artifacts)
        
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["pr_url"], "https://github.com/test/repo/pull/1")
        self.assertEqual(res["pr_number"], 1)
        self.assertEqual(res["files_committed"], 1)
        self.assertEqual(res["branch"], "praxis/trust-remediation-run_1234")
        
        # Assert calls
        mock_repo.create_git_ref.assert_called_once_with(ref="refs/heads/praxis/trust-remediation-run_1234", sha="abcdef123456")
        mock_repo.create_file.assert_called_once()
        mock_repo.create_pull.assert_called_once()

if __name__ == "__main__":
    unittest.main()
