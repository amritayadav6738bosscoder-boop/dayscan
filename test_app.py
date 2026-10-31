import unittest
from unittest.mock import Mock, patch

import app as dayscan


class DayScanTests(unittest.TestCase):
    def setUp(self):
        dayscan.app.config["TESTING"] = True
        self.client = dayscan.app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"DayScan", response.data)

    def test_rejects_non_list_tasks(self):
        response = self.client.post("/api/suggest", json={"tasks": "study"})
        self.assertEqual(response.status_code, 400)

    def test_rejects_empty_tasks(self):
        response = self.client.post("/api/suggest", json={"tasks": []})
        self.assertEqual(response.status_code, 400)

    @patch("app.requests.post")
    def test_returns_local_model_suggestion(self, mock_post):
        fake_response = Mock()
        fake_response.json.return_value = {"response": "Start with revising one topic."}
        fake_response.raise_for_status.return_value = None
        mock_post.return_value = fake_response

        response = self.client.post("/api/suggest", json={"tasks": ["Revise AI agents"]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["suggestion"], "Start with revising one topic.")
        self.assertEqual(response.get_json()["model"], dayscan.OLLAMA_MODEL)
        mock_post.assert_called_once()

    @patch("app.requests.post")
    def test_reports_ollama_unavailable(self, mock_post):
        import requests
        mock_post.side_effect = requests.ConnectionError("Ollama is down")

        response = self.client.post("/api/suggest", json={"tasks": ["Study"]})

        self.assertEqual(response.status_code, 503)
        self.assertIn("Could not reach Ollama", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
