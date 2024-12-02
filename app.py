from flask import Flask, render_template, request, session
import json
from database import database
from blueprints import books
from cli import create_all, drop_all, populate

from api.api_utils import fetch_book_details

app = Flask(__name__)
app.secret_key = 'abc'

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
app.register_blueprint(books)

with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)


if __name__ == "__main__":
    app.debug = True
    app.run()


def get_book_url(book):
    return r"https://covers.openlibrary.org/b/isbn/" + book["isbn"] + "-M.jpg"


# METHOD WILL BECOME A DATABASE QUERY
def get_books():
    # Open the file and parse the JSON data
    try:
        with open("./static/books.json") as file:
            books = json.load(file) # JSON data -> dictionary 
    except FileNotFoundError:
        raise FileNotFoundError("The file 'static/books.json' was not found.")
    except json.JSONDecodeError:
        raise ValueError("The file contains invalid JSON.")

    for bk in books:
        if isinstance(bk, dict) and "isbn" in bk:
            bk["cover_image_url"] = get_book_url(bk)
        else:
            raise ValueError(f"Invalid book entry: {bk}")

    return books


def get_book_from_isbn(books, isbn):
    for bk in books:
        if bk['isbn'] == isbn:
            return bk


# make books a global variable
books = get_books()


@app.route("/", methods=["GET", "POST"])
def index():
    # books = get_books()  # REFRESH - WILL REPLACE WITH QUERYING DATABASE
    if request.method == "POST":
        book_data = session.pop('book_data', None)
        book_data['email'] = request.form.get('email', None)
        books.append(book_data)
        # STORE in database
    return render_template("index.html", books=books)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        title = request.form.get("title")

        # call api
        book_data = fetch_book_details(title)
        session['book_data'] = book_data

        # set return route for cancel
        return_route = "/add"
    else:
        isbn = request.args.get("isbn")
        book_data = get_book_from_isbn(books, isbn)
        return_route = "/"

    return render_template("details.html", result=book_data,
                           return_route=return_route)


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
