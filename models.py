from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


# ----------------------------------------------------------------- #
# App Config.
# ----------------------------------------------------------------- #

database_name = "casting_agency"
# # for local use:
# database_path = "postgres://{}:{}@{}/{}".format(
#     'student', 'student', 'localhost:5432', database_name)

# For heroku:
database_path = os.getenv("DATABASE_URL")

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# ----------------------------------------------------------------- #
# Models.
# ----------------------------------------------------------------- #

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)

    # define dunder repr method to help in db troubleshooting
    def __repr__(self):
        return f"<Movie id='{self.id}' title='{self.title}'>"

    # class initialization
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    # function to insert new movie
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # funciton to update an existing movie
    def update(self):
        db.session.commit()

    # delete movie
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # format the returned value for a movie
    #  record
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


class Actors(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(30))

    # define dunder repr method to help in db troubleshooting
    def __repr__(self):
        return f"<Actor id: '{self.id}' name: '{self.name}'>"

    # Class initilization
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    # insert new actor
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update on actor record
    def update(self):
        db.session.commit()

    # delete actor record
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # format the returned value for an actor record
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}
