from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def process_query(query):
    if query.lower() == "pi":
        return "pi is an irrational number"
    elif query == "Who is the author of LOTR":
        return "J.R.R. Tolkein"
    return "UNKNOWN"

def get_books():
    return


def get_book_url():
    return


@app.route("/", methods=["GET"])
def query():
    return process_query(request.args.get('q'))
