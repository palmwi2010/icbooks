from database import database as db

#  model says "this class is a table"
# "need to define column" -> email, book title, book author
class Book(db.Model):

    #__tablename__ = "books"

    #id = database.Column(db.Integer, primary_key=True) #example of primary key
    email_user = db.Column(db.String, nullable=False)
    book_cover = db.Colum(db.String, nullable=True)
    title = db.Column(db.String, nullable=False )
    author = db.Column(db.String, nullable=False)
    #swap = db.Column(db.Boolean, default=False)
