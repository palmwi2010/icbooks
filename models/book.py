from icnews.database import database as db


#  model says "this class is a table"
# "need to define column" -> email, book title, book author
class Book(db.Model):

    # __tablename__ = "books"

    isbn = db.Column(db.Integer, primary_key=True)  # example of primary key
    email = db.Column(db.String, nullable=False)
    cover_image_url = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    authors = db.Column(db.String, nullable=False)
    publish_date = db.Column(db.String, nullable=True)
    first_sentence = db.Column(db.String, nullable=True)
    subject = db.Column(db.String, nullable=True)
