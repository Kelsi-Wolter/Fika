'''Models for MN Coffee Roasters App'''

# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_login import LoginManager



# app = Flask(__name__)
db = SQLAlchemy()

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


    # backref='lists'

class Roaster(db.Model):
    '''A Coffee Roaster'''

    __tablename__ = 'roasters'

    roaster_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    hours = db.Column(db.String(300))
    image = db.Column(db.String(200))
    website = db.Column(db.String(100))
    coffee_link = db.Column(db.String(40))
    shipping_link = db.Column(db.String(40))
    
    

    def __repr__(self):
        return f'<Roaster roaster_ID={self.roaster_id} name={self.name}>'

    # backref='entries'


class List(db.Model):
    '''List built by user to keep track of roasters'''

    __tablename__ = 'lists'

    list_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    list_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref='lists')
    entries = db.relationship('Entry')    
 

    def __repr__(self):
        return f'<List list_ID={self.list_id} list_name={self.list_name}>'


class Entry(db.Model):
    '''Entry onto list (includes rating for roaster)'''

    __tablename__ = 'entries'

    entry_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'), nullable=False)
    roaster_id = db.Column(db.Integer, db.ForeignKey('roasters.roaster_id'), nullable=False)
    score = db.Column(db.Float)
    note = db.Column(db.Text)

    entry_list = db.relationship('List')
    roaster = db.relationship('Roaster', backref='entries')    
 

    def __repr__(self):
        return f'<Entry entry_id={self.entry_id} score={self.score} roaster={self.roaster.name} list={self.entry_list.list_name} author={self.entry_list.user_id}>'


class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')

class NewUserForm(FlaskForm):
    fname = StringField('first')
    lname = StringField('last')
    email = StringField('email')
    password = PasswordField('password')



'''Copied from model.py in ratings app that connects to the database'''

def connect_to_db(flask_app, db_uri='postgresql:///MNroasters', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    #flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)

