'''Models for MN Coffee Roasters App'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    '''A user'''

    __tablename__ = __users__

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

class Rating(db.Model):
    '''Rating from user on coffee roaster'''

class List(db.Model):
    '''List built by user to keep track of roasters they've tried'''