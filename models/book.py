from ..database import database as db


# Set structure of Book model in db
class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    cover_image_url = db.Column(db.String, nullable=True)
    cached_url = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    authors = db.Column(db.String, nullable=True)
    publish_date = db.Column(db.String, nullable=True)
    first_sentence = db.Column(db.String, nullable=True)
    subject = db.Column(db.String, nullable=True)
