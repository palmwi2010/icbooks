from flask import Flask, render_template
from database import database
from blueprints import books
from cli import create_all, drop_all, populate

app = Flask(__name__)
# connection to real data base
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://tg1424:7J4b3q,7y4kG86@db.doc.ic.ac.uk/tg1424"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
print("IM DOING SOMETHING")
# initialisation of database object (instance of SQLAlchemy)
# with Flask application (app)
# links SQLAlchemy with the Flask app so that the app can interact
# with the specified database using SQLAlchemy
database.init_app(app)

# Register Blueprints
app.register_blueprint(books)

with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
