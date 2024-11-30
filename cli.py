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
            cover_image_url="https://m.media-amazon.com/images/I/"
            "71H2SJik5AL._SY342_.jpg",
            title="The Book Thief",
            authors="Markus Zusak",
            publish_date="2020",
            first_sentence="It was a cold, quiet evening when the book"
            "first arrived.",
            subject="Fiction, Fantasy, Adventure",
        ),
        Book(
            isbn="0446310786",  # 0 missing before 44
            email="alfonso.gambino24@imperial.ac.uk",
            cover_image_url="https://m.media-amazon.com/images/I/71FxgtFKcQL"
            "._SY342_.jpg",
            title="To Kill a Mockingbird",
            authors="Harper Lee",
            publish_date="1960",
            first_sentence="The sun was setting over the quiet town, casting"
            "long shadows on the dusty streets.",
            subject="Fiction, Fantasy, Adventure",
        ),
    ]
    for book in initial_books:
        database.session.add(book)

    database.session.commit()
