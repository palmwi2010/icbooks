from flask import Blueprint, request, render_template
# may want to import redirect, url_for, abort

# Constructs a SQL SELECT query for retrieving data from the databas
from sqlalchemy import select

# Imports the database object (an instance of SQLAlchemy),
# which manages the connection to the database
# and provides methods to interact with it.
from ..database import database

# Imports the Book model, which maps to a table in the database
# (likely representing books).
# Each instance of Book corresponds to a row in the database.
from ..models.book import Book


# All routes in this Blueprint will have URLs prefixed with /books
# reminder for Tiago: The __name__ variable is a special built-in
# variable in Python that refers to the name of the current module (or file)
books = Blueprint("books", __name__, url_prefix="/books")


@books.route("/addbook", methods=["GET", "POST"])
def all():
    if request.method == "POST":
        print("Adding book")
        print(request.form["isbn"])
        database.session.add(
            Book(
                # this is where data is extracted
                # from submitted form HTTP POST request
                isbn=request.form["isbn"],
                title=request.form["book-title"],
                authors=request.form["author-subtitle"],
                email=request.form["email"],
                publish_date=request.form["published_date"]
                # book_cover=request.form["book_cover"],
            )
        )
        database.session.commit()

    # Retrieve books from the database
    all_books = database.session.execute(select(Book)).all()
    return render_template("details.html", result=all_books[-1])
