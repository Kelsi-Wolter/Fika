'''Models for MN Coffee Roasters App'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    '''A user'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.first_name} {self.last_name}>'


class Roaster(db.Model):
    '''A Coffee Roaster'''

    __tablename__ = 'roasters'

    roaster_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(200))
    avg_user_rating = db.Column(db.Float)
    shipping = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Roaster roaster_ID={roaster_id} name={name}>'

class Rating(db.Model):
    '''Rating from user on coffee roaster'''

    pass

class List(db.Model):
    '''List built by user to keep track of roasters they've tried'''

    pass



'''Copied from model.py in ratings app that connects to the database'''

def connect_to_db(app, MNroasters, echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    flask_app.config['SQLALCHEMY_ECHO'] = False
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False (True)) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)