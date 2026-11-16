import unittest
from app import app
from unittest.mock import patch, Mock


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    @patch("app.requests.get")
    def test_search(self, mock_get):

        mock_response = Mock()
        mock_response.json.return_value = {
            "organic_results": [
                {
                    "title": "Programming",
                    "link": "https://example.com"
                }
            ]
        }

        mock_get.return_value = mock_response

        response = self.client.post(
            "/search",
            data={"keyword": "PLC programování"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.get_json()[0]["title"],
            "Programming"
        )

    def test_search_empty_keyword(self):

        response = self.client.post(
            "/search",
            data={"keyword": ""}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.get_json()["error"],
            "Chybí klíčové slovo"
        )

    def test_search_whitespace_keyword(self):

        response = self.client.post(
            "/search",
            data={"keyword": "   "}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.get_json()["error"],
            "Chybí klíčové slovo"
        )