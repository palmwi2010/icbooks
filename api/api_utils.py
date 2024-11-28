import requests


def fetch_book_details(user_input):
    # Validate input
    user_input = user_input.strip()
    if not user_input:
        return {"error": "Search term is required"}

    # API url
    base_url = "https://openlibrary.org/search.json"

    # Make the API request
    try:
        response = requests.get(base_url, params={"q": user_input})
        # Raises an error if the API is not responding
        response.raise_for_status()
    except requests.exeptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

    # Parse JSON response
    data = response.json()

    # Check for results
    if not data.get("docs"):
        return {"message": "No matching books found"}

    # Extract the first result
    book = data["docs"][0]
    cover_id = book.get("cover_i", None)
    cover_image_url = (
        f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        if cover_id else None
    )
    title = book.get("title", "Unkown Title")
    authors = book.get("author_name", ["Unkown Author"])

    # Return book details
    return {
        "cover_image_url": cover_image_url,
        "authors": authors,
        "title": title
    }
