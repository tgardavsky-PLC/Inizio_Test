import unittest
from app import app
from unittest.mock import patch, Mock, mock_open


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    @patch("app.requests.get")
    def test_search(self, mock_get):

        expected_results = [
            {
                "title": "Programming",
                "link": "https://example.com"
            }
        ]

        mock_response = Mock()
        mock_response.json.return_value = {
            "organic_results": expected_results
        }

        mock_get.return_value = mock_response

        with patch("app.API_KEY", "test-api-key"):
            with patch("builtins.open", mock_open()) as mocked_file:
                with patch("app.json.dump") as mocked_dump:

                    response = self.client.post(
                        "/search",
                        data={"keyword": "PLC programování"}
                    )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.get_json(), expected_results)

        self.assertEqual(
            response.get_json()[0]["title"],
            "Programming"
        )

        self.assertEqual(
            response.get_json()[0]["link"],
            "https://example.com"
        )

        mock_get.assert_called_once()

        self.assertEqual(
            mock_get.call_args.kwargs["params"]["engine"],
            "google"
        )

        self.assertEqual(
            mock_get.call_args.kwargs["params"]["q"],
            "PLC programování"
        )

        mocked_file.assert_called_once_with(
            "results.json",
            "w",
            encoding="utf-8"
        )

        mocked_dump.assert_called_once_with(
            expected_results,
            mocked_file(),
            ensure_ascii=False,
            indent=4
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
