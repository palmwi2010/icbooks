from flask import Flask, request, render_template
import json


# from api.api_utils import fetch_book_details

app = Flask(__name__)


def get_book_url(book):
    return r"https://covers.openlibrary.org/b/isbn/" + book['isbn'] + "-M.jpg"


# METHOD WILL BECOME A DATABASE QUERY
def get_books():
    with open('./static/books.json') as file:
        books = json.load(file)["books"]
        for bk in books:
            bk['url'] = get_book_url(bk)
        return books


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # QUERY API AGAIN and STORE in database
        pass
    books = get_books()  # WILL REPLACE WITH QUERYING DATABASE
    return render_template("index.html", books=books)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        title = request.form.get("title")
        email = request.form.get("email")
        # CALL API TO GET result dict
        return_route = "/add"
    else:
        title = request.args.get("title")
        email = request.args.get("email")
        # QUERY DATABASE TO GET DATA
        return_route = "/"
    return render_template("details.html", title=title, email=email,
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
    return process_query(request.args.get('q'))
