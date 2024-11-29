from flask import Flask, request, render_template, session
import json

from api.api_utils import fetch_book_details


# from api.api_utils import fetch_book_details

app = Flask(__name__)
app.secret_key = 'abc'


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


@app.route("/query", methods=["GET"])  # Do we need "POST" as well?
def query():
    return process_query(request.args.get("q"))
