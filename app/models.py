# Add any model classes for Flask-SQLAlchemy here
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash

class Users(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'Users'

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