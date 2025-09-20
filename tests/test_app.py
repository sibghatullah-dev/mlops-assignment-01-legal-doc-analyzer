# Testing Jenkins CI/CD pipeline
import unittest
import json
from app.app import app


class TestLegalDocAnalyzer(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_analyze_endpoint(self):
        test_data = {
            "contract_text": "This agreement shall be governed by California law."
        }
        response = self.app.post(
            "/analyze", data=json.dumps(test_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("risk_score", data)
        self.assertIn("flagged", data)
        self.assertIn("explanation", data)

    def test_missing_text(self):
        response = self.app.post(
            "/analyze", data=json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
