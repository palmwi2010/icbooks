from ..app import app
import requests
from unittest.mock import patch
from api.api_utils import fetch_book_details


def test_homepage_loads_correctly():
    # Create a test client to allow simulation of HTTP requests to the app
    with app.test_client() as client:
        response = client.get("/")

    # Assert the request succeeded (HTTP 200)
    assert response.status_code == 200


# API tests:
# Test sucessful response from API and parsing of returned data
def test_fetch_book_details_success():
    # Mock successful API response
    mock_response = {
        "docs": [
            {
                "cover_i": 14625765,
                "title": "The Lord of the Rings",
                "author_name": ["J.R.R Tolkein", "No Other"],
                "isbn": ["9781611748864"],
                "first_publish_year": 1954,
                "first_sentence": ["This is a test sentence."],
                "subject": ["Fantasy", "Fiction", "Not in list"],
            }
        ]
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        from api.api_utils import fetch_book_details

        book_details = fetch_book_details("Test Book")

        assert book_details["success"] == 0
        assert book_details["title"] == "The Lord of the Rings"
        assert book_details["authors"] == (
            "J.R.R Tolkein, No Other"
        )  # join
        assert book_details["isbn"] == "9781611748864"
        assert book_details["cover_image_url"] == (
            "https://covers.openlibrary.org/b/id/14625765-M.jpg"
        )  # construct url
        assert book_details["publish_date"] == 1954
        assert book_details["first_sentence"] == "This is a test sentence."
        assert book_details["subject"] == (
            "Fantasy, Fiction"
        )  # join with filtering


# Test failed response from API and parsing of returned data
def test_error_in_api_raised_correctly():
    # Mock a failed API response
    with patch("requests.get") as mock_get:
        # Simulate an exception during the API call
        mock_get.side_effect = requests.exceptions.RequestException(
            "Network error"
        )

        book_details = fetch_book_details("Test Book")

        # Assertions to verify the error is handled correctly
        assert book_details["success"] == -1
        assert book_details["error"] == "API request failed: Network error"


def test_fetch_book_details_no_results():
    # Mock API response with no results
    mock_response = {"docs": []}

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        from api.api_utils import fetch_book_details

        book_details = fetch_book_details("siahdlidnflbdnb")

        assert "error" in book_details
        assert book_details["success"] == -2
        assert book_details["error"] == "No matching books found"
