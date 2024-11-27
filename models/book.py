from database import database as db

#needs to be changed. maybe our class is going to be something like "BookSubmission" -> email, book title, book author
class Book(db.Model):
    book_cover = db.Colum(db.String)
    title = db.Column(db.String)
    author = db.Column(db.String)
