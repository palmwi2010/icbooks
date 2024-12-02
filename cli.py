import click
from flask.cli import with_appcontext

from database import database
from models import Book


@click.command("create_all", help="Create all tables in the app's database")
@with_appcontext
def create_all():
    database.create_all()


@click.command("drop_all", help="Drop all tables in the specified database")
@with_appcontext
def drop_all():
    database.drop_all()


@click.command("populate", help="Populate the database with initial data")
@with_appcontext
def populate():
    initial_books = [
        Book(
            isbn="9780552773898",
            email="william.palmer24@imperial.ac.uk",
            cover_image_url=(
                "https://covers.openlibrary.org/b/isbn/9780552773898-M.jpg"
            ),
            title="The Book Thief",
            authors="Markus Zusak",
            publish_date="2020",
            first_sentence="It was a cold, quiet evening when the book",
            subject="Fiction, Fantasy, Adventure",
        ),
        Book(
            isbn="9780061120084",
            email="alfonso.gambino24@imperial.ac.uk",
            cover_image_url=(
                "https://covers.openlibrary.org/b/isbn/9780061120084-M.jpg",
            ),
            title="To Kill a Mockingbird",
            authors="Harper Lee",
            publish_date="1960",
            first_sentence="First sentence.",
            subject="Fiction, Fantasy, Adventure",
        ),
    ]
    for book in initial_books:
        database.session.add(book)

    database.session.commit()
