from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def process_query(query):
    if query.lower() == "pi":
        return "pi is an irrational number"
    elif query == "Who is the author of LOTR":
        return "JRR Tolkein"
    return "UNKNOWN"


@app.route("/query", methods=["GET"])  # Do we need "POST" as well?
def query():
    return process_query(request.args.get('q'))
