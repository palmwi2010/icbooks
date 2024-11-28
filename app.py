from flask import Flask, request, render_template
import json


app = Flask(__name__)


def get_book_url(book):
    return r"https://covers.openlibrary.org/b/isbn/" + book['isbn'] + "-M.jpg"


def get_books():
    with open('./static/books.json') as file:
        books = json.load(file)["books"]
        for bk in books:
            bk['url'] = get_book_url(bk)
        return books


@app.route("/")
def index():
    books = get_books()
    return render_template("index.html", books=books)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/about")
def about():
    return render_template("about.html")

def process_query(query):
    if query.lower() == "pi":
        return "pi is an irrational number"
    elif query == "Who is the author of LOTR":
        return "JRR Tolkein"
    return "UNKNOWN"


@app.route("/query", methods=["GET"])  # Do we need "POST" as well?
def query():
    return process_query(request.args.get('q'))
