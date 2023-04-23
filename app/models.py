# Add any model classes for Flask-SQLAlchemy here

from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password= db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    biography = db.Column(db.String(1000), nullable=False)
    profile_photo = db.Column(db.String(200), nullable=False)
    joined_on = db.Column(db.DateTime, nullable=False, default=datetime.now())

    #relationships between user, posts and followers
    posts= db.relationship('Posts', backref='Users', passive_deletes=True, lazy=True)
    likes= db.relationship('Likes', backref='Users', passive_deletes= True, lazy= True)
    followers= db.relationship('Follows', backref= 'Users', passive_deletes= True, lazy= True)

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username= username
        self.password= generate_password_hash(password, method='pbkdf2:sha256')
        self.first_name= firstname
        self.last_name= lastname
        self.email= email
        self.location= location
        self.biography= biography
        self.profile_photo= profile_photo

class Posts(db.Model):
    __tablename__= "Posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())




