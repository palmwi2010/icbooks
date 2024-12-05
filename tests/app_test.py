from ..app import app, database
from flask import Flask, session, request
from ..api.api_utils import fetch_book_details
from unittest.mock import mock_open, patch, MagicMock
import json
from ..models.book import Book


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
        assert book_details["authors"] == "J.R.R Tolkein, No Other"  # join
        assert book_details["isbn"] == "9781611748864"
        assert book_details["cover_image_url"] == (
            "https://covers.openlibrary.org/b/id/14625765-M.jpg") #construct url
        assert book_details["publish_date"] == 1954
        assert book_details["first_sentence"] == "This is a test sentence."
        assert book_details["subject"] == "Fantasy, Fiction" # join with filtering


#def test_error_in_api_raised_correctly(): api_utils line 34-36
    

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


def test_add_book():
    mock_database_session = MagicMock()
    mock_commit = MagicMock()

    book_data = {
        "isbn": "9780552773898",
        "email": "william.palmer24@imperial.ac.uk",
        "cover_image_url": "https://covers.openlibrary.org/b/isbn/9780552773898-M.jpg",
        "title": "The Book Thief",
        "authors": "Markus Zusak",
        "publish_date": "2020",
        "first_sentence": "It was a cold, quiet evening when the book",
        "subject": "Fiction, Fantasy, Adventure",
    }

    # Mock database session methods
    with patch("app.database.session", mock_database_session):
        mock_database_session.commit = mock_commit

        # Use Flask test client to simulate a POST request
        with app.test_client() as client:
            response = client.post("/add", data=book_data)

            # Assert session's add method was called with a Book object
            mock_database_session.add.assert_called_once()
            added_book = mock_database_session.add.call_args[0][0]

            # Validate that added_book is a Book instance with correct attributes
            assert isinstance(added_book, Book)
            assert added_book.isbn == book_data["isbn"]
            assert added_book.title == book_data["title"]
            assert added_book.authors == book_data["authors"]
            assert added_book.email == book_data["email"]

            # Ensure commit was called
            mock_commit.assert_called_once()

            # Verify that the response redirects to the homepage
            assert response.status_code == 302
            assert response.location == "/"
 
"""
def test_get_books_from_database():
    # Mock database query
    mock_books = [
        Book(isbn="123", title="Test Book 1", authors="Author 1"),
        Book(isbn="456", title="Test Book 2", authors="Author 2"),
    ]
    with patch("database.database.session.execute") as mock_execute:
        mock_execute.return_value.all.return_value = mock_books

        from blueprints.books import all as get_books
        with app.test_client() as client:
            response = client.get("/books/addbook")

        # Assert books are fetched correctly
        assert len(response.context["result"]) == len(mock_books)

        """
