from flask import Flask, request, render_template
import json

app = Flask(__name__)

def get_book_url(book):
    return r"https://covers.openlibrary.org/b/isbn/" + book['isbn'] + "-M.jpg"

def get_books(search_term = None):
    with open('./static/books.json') as file:
        books = json.load(file)["books"]
        for bk in books:
            bk['url'] = get_book_url(bk)
        return books

@app.route("/", methods = ["GET", "POST"])
def index():
    books = get_books()
    return render_template("index.html", books = books)

@app.route("/add", methods = ["GET", "POST"])
def add():
    return render_template("add.html")