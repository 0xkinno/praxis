import unittest
from fastapi.testclient import TestClient
from praxis.config import settings
from praxis.api.main import app

class TestAPIEndpoints(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Force fixture mode for API unit testing
        settings.mode = "fixture"
        cls.client = TestClient(app)
        
    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["mode"], "fixture")
        
    def test_catalog_overview(self):
        response = self.client.get("/api/catalog/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_datasets"], 52)
        self.assertEqual(data["total_dashboards"], 12)
        self.assertIn("trusted", data["tier_distribution"])
        
    def test_assessments_list(self):
        response = self.client.get("/api/assessments")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["run_id"], "run_9f8d7c")
        
    def test_assessment_details(self):
        response = self.client.get("/api/assessments/run_9f8d7c")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "completed")
        self.assertEqual(data["run_id"], "run_9f8d7c")
        
    def test_assessment_details_not_found(self):
        response = self.client.get("/api/assessments/run_missing")
        self.assertEqual(response.status_code, 404)
        
    def test_assets_list(self):
        response = self.client.get("/api/assets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["name"], "order_details")
        
    def test_assets_list_filter(self):
        response = self.client.get("/api/assets?domain=Analytics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for asset in data:
            self.assertEqual(asset["domain"], "Analytics")
            
    def test_asset_trust_history(self):
        urn = "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)"
        response = self.client.get(f"/api/assets/{urn}/trust")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["urn"], urn)
        
    def test_asset_artifacts(self):
        urn = "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)"
        response = self.client.get(f"/api/assets/{urn}/artifacts")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["target_urn"], urn)
        
    def test_asset_propagation(self):
        urn = "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)"
        response = self.client.get(f"/api/assets/{urn}/propagation")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_affected"])
        self.assertTrue(len(data["propagation_path"]) > 0)
        
    def test_domains_list(self):
        response = self.client.get("/api/domains")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]["domain"], "Analytics")
        
    def test_domain_assets(self):
        response = self.client.get("/api/domains/Analytics/assets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        
    def test_contracts_list(self):
        response = self.client.get("/api/contracts")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        
    def test_contract_download(self):
        response = self.client.get("/api/contracts/1/download")
        self.assertEqual(response.status_code, 200)
        self.assertIn("order_details", response.text)
        
    def test_contract_download_not_found(self):
        response = self.client.get("/api/contracts/99/download")
        self.assertEqual(response.status_code, 404)
        
    def test_ml_check_training_data_block(self):
        payload = ["urn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)"]
        response = self.client.post("/api/ml/check-training-data", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["verdict"], "BLOCK_TRAINING")
        self.assertTrue(len(data["upstream_risks"]) > 0)
        
    def test_ml_check_training_data_safe(self):
        payload = ["urn:li:dataset:(urn:li:dataPlatform:mysql,checkout.stock_levels,PROD)"]
        response = self.client.post("/api/ml/check-training-data", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["verdict"], "SAFE_TO_TRAIN")
        self.assertEqual(len(data["upstream_risks"]), 0)
        
    def test_latest_propagation(self):
        response = self.client.get("/api/propagation/latest")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["untrusted_sources"], 2)
        
    def test_digests_list(self):
        response = self.client.get("/api/digests")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        
    def test_digest_content(self):
        response = self.client.get("/api/digests/run_9f8d7c")
        self.assertEqual(response.status_code, 200)
        self.assertIn("# PRAXIS Daily Intelligence Digest", response.text)

if __name__ == "__main__":
    unittest.main()
