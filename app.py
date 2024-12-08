from flask import Flask, render_template, request, redirect
from sqlalchemy import select

from .database import database
from .models.book import Book
from .cli import create_all, drop_all, populate
from .api.api_utils import fetch_book_details, validate_email

app = Flask(__name__)
app.secret_key = "abc"

# connection to real database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://tg1424:7J4b3q,7y4kG86@db.doc.ic.ac.uk/tg1424"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialise database object (instance of SQLAlchemy)
database.init_app(app)

with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)


@app.route("/")
def index():
    books = database.session.execute(select(Book)).scalars()
    return render_template("index.html", books=books)


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/add", methods=["POST"])
def add():
    # server side validation on email provided
    if not validate_email(request.form.get("email")):
        return redirect("/")  # redirect back home - html was tampered with

    try:
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
    except Exception as e:
        print(f"Error occurred adding to database: ${e}")
        return render_template("apology.html")  # error on add to database
    return redirect("/")


@app.route("/details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        title = request.form.get("title")

        # fetch from api
        book_data = fetch_book_details(title)
        success_code = book_data.get("success")  #
        print(success_code)

        # -1 indicates error fulfilling api call
        if success_code == -1:
            return render_template("apology.html")

        # No book empty: return to search page
        if success_code == -2:
            return render_template(
                "search.html", feedback="Could not find requested book."
            )

        return_route = "/search"
    else:
        id = request.args.get("id")

        # fetch from database
        book_data = database.get_or_404(Book, id, description="Book not found")
        return_route = "/"

    return render_template(
        "details.html",
        result=book_data,
        return_route=return_route)


@app.route("/about")
def about():
    return render_template("about.html")
