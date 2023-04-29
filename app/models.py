# Add any model classes for Flask-SQLAlchemy here
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash

class Users(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password= db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    biography = db.Column(db.String(1000), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    joined_on = db.Column(db.DateTime(), nullable=False)

    def __init__(self, username, password, firstname, lastname, email, location, biography, photo):
        self.username= username
        self.password= generate_password_hash(password, method='pbkdf2:sha256')
        self.firstname= firstname
        self.lastname= lastname
        self.email= email
        self.location= location
        self.biography= biography
        self.photo= photo
        self.joined_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    
class Posts(db.Model):
    __tablename__= "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,)

    #relationship between posts and likes
    likes= db.relationship('Likes', backref='Posts', passive_deletes= True, lazy=True)

    def __init__(self, user_id, photo, caption):
        self.photo= photo
        self.caption= caption
        self.user_id= user_id
        self.created_on= datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
class Likes(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(Posts.id, ondelete='CASCADE'), nullable=False)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
class Follows(db.Model):
    __tablename__ = "follows"
    __table_args__ = (db.UniqueConstraint('user_id', 'follower_id', name='_user_follower_uc'), )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    follower_id = db.Column(db.Integer, nullable=False)

    def __init__(self, follower_id, user_id):
        self.follower_id = follower_id
        self.user_id = user_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id) # python 3 support