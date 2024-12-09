from flask import Flask, render_template, request, redirect
from sqlalchemy import select
from dotenv import load_dotenv
import os

from .database import database
from .models.book import Book
from .cli import create_all, drop_all, populate
from .api.api_utils import (
    fetch_book_details,
    validate_email,
    update_cache,
    save_img
)

# initialise app
app = Flask(__name__)

# load env variables which includes database uri
load_dotenv()

# connection to real database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialise database object (instance of SQLAlchemy)
database.init_app(app)

# set cli commands
with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)


@app.route("/")
def index():
    """Home page displaying all books loaded"""
    # get books from database
    books = database.session.execute(select(Book)).scalars()
    return render_template("index.html", books=books)


@app.route("/search")
def search():
    """Route to search for a book"""
    return render_template("search.html")


@app.route("/add", methods=["POST"])
def add():
    """Post method to add a book to db"""
    # server side validation on email provided
    if not validate_email(request.form.get("email")):
        return redirect("/")  # redirect back home - html was tampered with
    try:
        # cache the book image
        save_img(request.form.get("cover_image_url"))

        # save book to database
        database.session.add(
            Book(
                isbn=request.form.get("isbn"),
                email=request.form.get("email"),
                cover_image_url=request.form.get("cover_image_url"),
                cached_url=request.form.get("cached_url"),
                title=request.form.get("title"),
                authors=request.form.get("authors"),
                publish_date=request.form.get("publish_date"),
                first_sentence=request.form.get("first_sentence"),
                subject=request.form.get("subject"),
            )
        )
        database.session.commit()

    # handle exception by showing error page
    except Exception as e:
        print(f"Error occurred adding to database: ${e}")
        return render_template("apology.html")  # error on add to database

    # redirect user back to home page
    return redirect("/")


@app.route("/details", methods=["GET", "POST"])
def details():
    """Book details with confirmation to add if it is a POST"""
    if request.method == "POST":
        # get book title
        title = request.form.get("title")

        # fetch from api
        book_data = fetch_book_details(title)
        success_code = book_data.get("success")  #

        # -1 indicates error fulfilling api call
        if success_code == -1:
            return render_template("apology.html")

        # No book empty: return to search page
        if success_code == -2:
            return render_template(
                "search.html", feedback="Could not find requested book."
            )

        # back button takes you back to search page if a POST
        return_route = "/search"
    else:
        # get book id
        id = request.args.get("id")

        # fetch from database
        book_data = database.get_or_404(Book, id, description="Book not found")
        return_route = "/"  # back to home page if accessed by GET

    return render_template(
        "details.html",
        result=book_data,
        return_route=return_route
        )


@app.route("/about")
def about():
    """About page for ICBooks"""
    return render_template("about.html")


@app.route("/refresh_cache")
def refresh_cache():
    """Save books not in cache, remove from cache files no longer needed"""
    # get cover image urls
    cover_urls = database.session.execute(
        select(Book.cover_image_url)
        ).scalars()
    update_cache(cover_urls)  # updates the cache
    return redirect("/")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    """See all books and delete books from database"""
    if request.method == "POST":
        # get id of book to delete
        id = request.form.get("id-to-delete")

        # get book to delete
        book_to_delete = (
            database.session.execute(select(Book).filter(Book.id == id))
            .scalars()
            .first()
        )

        # delete book from db
        database.session.delete(book_to_delete)
        database.session.commit()

    # get all books in db
    books = database.session.execute(select(Book)).scalars()
    return render_template("delete.html", books=books)
