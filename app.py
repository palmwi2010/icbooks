from flask import Flask, render_template, request, session, redirect
import json
from database import database
from sqlalchemy import select
from models.book import Book
from blueprints import books
from cli import create_all, drop_all, populate

from api.api_utils import fetch_book_details

app = Flask(__name__)
app.secret_key = "abc"

# connection to real database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://tg1424:7J4b3q,7y4kG86@db.doc.ic.ac.uk/tg1424"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialisation of database object (instance of SQLAlchemy)
# with Flask application (app)
# links SQLAlchemy with the Flask app so that the app can interact
# with the specified database using SQLAlchemy
database.init_app(app)

# Register Blueprints
# app.register_blueprint(books)

with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)


def get_book_url(book):
    return r"https://covers.openlibrary.org/b/isbn/" + book["isbn"] + "-M.jpg"


# METHOD WILL BECOME A DATABASE QUERY
def get_books():
    with open("./static/books.json") as file:
        books = json.load(file)
        for bk in books:
            bk["cover_image_url"] = get_book_url(bk)
        return books


def get_book_from_isbn(books, isbn):
    for bk in books:
        if bk["isbn"] == isbn:
            return bk


@app.route("/", methods=["GET", "POST"])
def index():
    # books = get_books()  # REFRESH - WILL REPLACE WITH QUERYING DATABASE
    books = database.session.execute(select(Book)).scalars()
    if request.method == "POST":
        book_data = session.pop("book_data", None)
        book_data["email"] = request.form.get("email", None)
        books.append(book_data)
        # STORE in database
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        database.session.add(
            Book(
                isbn=request.form.get("isbn"),
                email=request.form.get("email"),
                cover_image_url=request.form.get("cover_image_url"),
                title=request.form.get("title"),
                authors=request.form.get("authors"),
                publish_date=request.form.get("publish_date"),
                first_sentence=request.form.get("first_sentence"),
                subject=request.form.get("subject"),
            )
        )
        database.session.commit()
        return redirect("/")
    return render_template("add.html")


@app.route("/details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        title = request.form.get("title")

        # call api
        book_data = fetch_book_details(title)
        session["book_data"] = book_data

        # set return route for cancel
        return_route = "/add"
    else:
        isbn = request.args.get("isbn")
        book_data = get_book_from_isbn(books, isbn)
        return_route = "/"

    return render_template(
        "details.html", result=book_data, return_route=return_route
        )


@app.route("/about")
def about():
    return render_template("about.html")


def process_query(query):
    if query.lower() == "pi":
        return "pi is an irrational number"
    elif query == "Who is the author of LOTR":
        return "J.R.R. Tolkein"
    return "UNKNOWN"


@app.route("/query", methods=["GET"])
def query():
    return process_query(request.args.get("q"))
