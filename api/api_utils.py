import requests
import re


def fetch_book_details(user_input):
    # Validate input
    user_input = user_input.strip()

    # API url
    base_url = "https://openlibrary.org/search.json"

    # List of all possible book genres (you can expand this list)
    predefined_genres = [
        "Fiction",
        "Fantasy",
        "Science Fiction",
        "Romance",
        "Thriller",
        "Crime",
        "Mystery",
        "Horror",
        "Biography",
        "History",
        "Self-Help",
        "Poetry",
        "Drama",
        "Young Adult",
    ]

    # Make the API request
    try:
        response = requests.get(
            base_url, params={"q": user_input, "language": "eng", "limit": 1}
        )
        # Raises an error if the API is not responding
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"success": -1,
                "error": f"API request failed: {e}"}

    # Parse JSON response
    data = response.json()

    # Check for results
    if not data.get("docs"):
        return {"success": -2,
                "error": "No matching books found"}

    # Extract the first result
    book = data["docs"][0]
    cover_id = book.get("cover_i", None)
    cover_image_url = (
        f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
        if cover_id else None
    )
    title = book.get("title", "Unknown Title")
    authors = ", ".join(book.get("author_name", "Unknown Author")[:3])  # max 3
    isbn = book.get("isbn", "ISBN Not Found")[0]
    publish_date = book.get("first_publish_year", "Publish Date Not Found")
    first_sentence = book.get("first_sentence", "Unknown First Sentence")[0]
    subject = book.get("subject", [])

    # Find matching generes
    matching_genre = [genre for genre in subject if genre in predefined_genres]

    # Return book details
    return {
        "success": 0,
        "cover_image_url": cover_image_url,
        "authors": authors,
        "title": title,
        "isbn": isbn,
        "publish_date": publish_date,
        "first_sentence": first_sentence,
        "subject": ", ".join(matching_genre),
    }


def validate_email(email):
    """Confirm an Email is a valid Imperial Email"""
    pattern = r'^[a-zA-Z0-9]+@ic\.ac\.uk$'
    return re.match(pattern, email) is not None
