from flask import Flask, render_template
from api.api_utils import fetch_book_details

app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template("index.html")