import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from praxis.agents.orchestrator import build_assessment_graph

class TestAgentsOrchestrator(unittest.TestCase):
    
    @patch("praxis.agents.census.PraxisDataHubClient")
    @patch("praxis.agents.assessor.genai.Client")
    @patch("praxis.agents.chronicler.PraxisWriter")
    @patch("praxis.agents.chronicler._get_previous_run_scores")
    @patch("praxis.agents.pr_agent.PraxisPRCreator")
    def test_full_graph_execution(self, mock_pr_creator_class, mock_prev_scores, mock_writer_class, mock_gemini_class, mock_datahub_client_class):
        # 1. Mock DataHub Client
        mock_client = MagicMock()
        mock_datahub_client_class.return_value = mock_client
        
        # Mock search counts
        mock_client.graph.execute_graphql.return_value = {
            "search": {"total": 5}
        }
        
        # Mock datasets returned by census
        target_urn = "urn:li:dataset:my_dataset"
        mock_client.get_all_datasets.return_value = [
            {
                "entity": {
                    "urn": target_urn,
                    "name": "my_dataset",
                    "platform": {"name": "hive"},
                    "ownership": {"owners": []},
                    "properties": {"description": ""},
                    "schemaMetadata": {
                        "fields": [
                            {"fieldPath": "id", "nullable": False, "description": "PK"}
                        ],
                        "primaryKeys": ["id"]
                    },
                    "glossaryTerms": {"terms": []},
                    "domain": None
                }
            }
        ]
        
        # Mock lineage
        mock_client.get_upstream_lineage.return_value = []
        mock_client.get_downstream_lineage.return_value = []
        
        # 2. Mock Gemini Client
        mock_gemini = MagicMock()
        mock_gemini_class.return_value = mock_gemini
        mock_response = MagicMock()
        mock_response.text = "This is a Gemini summary."
        mock_gemini.models.generate_content.return_value = mock_response
        
        # 3. Mock PR Agent Creator
        mock_pr_creator = MagicMock()
        mock_pr_creator_class.return_value = mock_pr_creator
        mock_pr_creator.create_remediation_pr.return_value = {
            "status": "skipped",
            "reason": "mock skip",
            "pr_url": None,
            "pr_number": None,
            "branch": None,
            "files_committed": 0
        }
        
        # 4. Mock Chronicler Writer
        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer
        mock_writer.write_trust_score.return_value = {"status": "success", "urn": target_urn}
        mock_writer.write_trust_tag.return_value = {"status": "success", "urn": target_urn}
        mock_writer.write_assessment_doc.return_value = {"status": "success", "urn": target_urn}
        mock_writer.save_document.return_value = "urn:li:post:123"
        
        # Mock DB previous scores
        mock_prev_scores.return_value = {}
        
        # 5. Compile and run Graph
        graph = build_assessment_graph()
        initial_state = {
            "run_id": "run_test_1234",
            "status": "running",
            "census": None,
            "entity_data": [],
            "lineage_data": {},
            "trust_scores": [],
            "propagation_result": None,
            "domain_health": [],
            "generated_artifacts": [],
            "pr_result": None,
            "writeback_results": [],
            "digest_content": None,
            "errors": [],
            "progress": {}
        }
        
        final_state = graph.invoke(initial_state)
        
        # Verify state completion
        self.assertIsNotNone(final_state["census"])
        self.assertEqual(final_state["census"].total_datasets, 5)
        self.assertEqual(len(final_state["trust_scores"]), 1)
        self.assertEqual(final_state["trust_scores"][0].urn, target_urn)
        
        # Score computation should yield D / 48.2
        self.assertEqual(final_state["trust_scores"][0].grade.value, "D")
        self.assertEqual(final_state["trust_scores"][0].composite_score, 48.2)
        
        # Remediations should be generated (score < 75)
        self.assertTrue(len(final_state["generated_artifacts"]) > 0)
        
        # Domain Health compiled
        self.assertEqual(len(final_state["domain_health"]), 1)
        self.assertEqual(final_state["domain_health"][0].domain, "Unassigned")
        
        # PR Result skipped
        self.assertEqual(final_state["pr_result"]["status"], "skipped")
        
        # Digest generated
        self.assertIsNotNone(final_state["digest_content"])
        self.assertIn("PRAXIS Daily Intelligence Digest", final_state["digest_content"])
        self.assertIn("run_test_1234", final_state["digest_content"])

if __name__ == "__main__":
    unittest.main()
