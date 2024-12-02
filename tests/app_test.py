from app import app, process_query, get_books, get_book_url
from unittest.mock import mock_open, patch
import json


def test_pi_lower():
    # Test "pi" query
    assert process_query("pi") == "pi is an irrational number"


def test_pi_upper():
    # Test case sensitivity
    assert process_query("PI") == "pi is an irrational number"


def test_knows_lotr_author():
    # Test a longer query
    assert process_query("Who is the author of LOTR") == "J.R.R. Tolkein"


def test_homepage_loads_correctly():
    # Create a test client to allow simulation of HTTP requests to the app
    with app.test_client() as client:
        response = client.get("/")

    # Assert the request succeeded (HTTP 200)
    assert response.status_code == 200


# API tests:
def test_get_books_with_mock_file():
    # Mock the content of the JSON file
    mock_json_data = """{"books": [{"title": "Book Title",
    "isbn": "123456789", "authors": "Anonymous"}]}"""

    # Temporarily replace the open() function with a mock version using patch
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        books = get_books()

    # Validate the mock book data
    url = "https://covers.openlibrary.org/b/isbn/123456789-M.jpg"
    assert len(books) == 1
    assert books[0]["title"] == "Book Title"
    assert books[0]["isbn"] == "123456789"
    assert books[0]["author"] == "Anonymous"
    assert books[0]["url"] == url


def test_get_books_reads_json_file():
    # Load the JSON file directly for comparison
    with open("./static/books.json") as file:
        expected_data = json.load(file)["books"]

    books = get_books()

    # Test for the first book in the list
    assert books[0]["isbn"] == expected_data[0]["isbn"]
    assert books[0]["cover_image_url"] == expected_data[0]["cover_image_url"]
    assert books[0]["authors"] == expected_data[0]["authors"]
    assert books[0]["title"] == expected_data[0]["title"]

    # Test for the last book in the list
    assert books[-1]["isbn"] == expected_data[-1]["isbn"]
    assert books[-1]["cover_image_url"] == expected_data[-1]["cover_image_url"]
    assert books[-1]["authors"] == expected_data[-1]["authors"]
    assert books[-1]["title"] == expected_data[-1]["title"]


def test_get_book_url_generates_correct_url():
    # Example book dictionary "The C Programming Language"
    book = {"isbn": "9780131103627"}

    expected_url = "https://covers.openlibrary.org/b/isbn/9780131103627-M.jpg"

    assert get_book_url(book) == expected_url


def test_books_have_correct_urls():
    # Check that the first and last entries have correct URLs
    books = get_books()

    expected_url_first = (
        "https://covers.openlibrary.org/b/isbn/" + books[0]["isbn"] + "-M.jpg"
    )
    assert books[0]["url"] == expected_url_first
    expected_url_last = (
        "https://covers.openlibrary.org/b/isbn/" + books[-1]["isbn"] + "-M.jpg"
    )
    assert books[-1]["url"] == expected_url_last
