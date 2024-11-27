from flask import Blueprint, request, render_template, redirect, url_for, abort

# Constructs a SQL SELECT query for retrieving data from the databas
from sqlalchemy import select

# Imports the database object (an instance of SQLAlchemy), which manages the connection to the database 
# and provides methods to interact with it.
from database import database

# Imports the Book model, which maps to a table in the database (likely representing books). 
# Each instance of Book corresponds to a row in the database.
from models.book import Book


# All routes in this Blueprint will have URLs prefixed with /books
# reminder for Tiago: The __name__ variable is a special built-in variable in Python that refers to the name of the current module (or file)
books = Blueprint("books", __name__, url_prefix="/books")

@books.route("/", methods =["GET", "POST"])
def all():
    if request.method == "POST":
        database.session.add(
            Book(
                title=request.form["book_title"],
                author=request.form["book_author"],
            )
        )
        database.session.commit()
    
    ### Fetch data from an external API
    #  api_url = "https://api.example.com/data"  ### Replace with the actual API URL
    #  response = requests.get(api_url)          ### Make a GET request to the API

    #Retrieve books from the database
    all_books = database.session.execute(select(Book)).scalars()
    return render_template("books.html", books= all_books)