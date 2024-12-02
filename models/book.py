from database import database as db


# Model tells us that the class is a table
class Book(db.Model):

    # __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=True)
    cover_image_url = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    authors = db.Column(db.String, nullable=True)
    publish_date = db.Column(db.String, nullable=True)
    first_sentence = db.Column(db.String, nullable=True)
    subject = db.Column(db.String, nullable=True)
