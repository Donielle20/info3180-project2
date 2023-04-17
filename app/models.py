# Add any model classes for Flask-SQLAlchemy here

from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class Posts(db.Model):
    __tablename__= "Posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())




