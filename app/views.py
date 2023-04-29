"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from flask import render_template, request, jsonify, send_file, g
import os
import psycopg2
from .forms import RegisterForm, LoginForm, PostsForm
from app.models import Users, Posts,Likes,Follows
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash
from app import app, db, login_manager
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
import jwt
from functools import wraps
import base64
from time import time
from datetime import datetime, timedelta
###
# Routing for your application.
###

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

        token = parts[1]

        try:
            app.logger.debug(app.config['SECRET_KEY'])
            payload = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = payload
        return f(*args, **kwargs)

    return decorated

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/register', methods=['POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            location = form.location.data
            biography = form.biography.data
            photo = form.photo.data

            filename = secure_filename(photo.filename)

            user = Users(username=username, password=password, firstname=firstname, lastname=lastname, email=email, location=location, biography=biography, photo=filename)
            db.session.add(user)
            db.session.commit()

            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return jsonify({"message": "User Successfully added","username": username})
        else:
            return jsonify({"errors": form_errors(form)})

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            username = form.username.data
            password = form.password.data
        
            user = db.session.execute(db.select(Users).filter_by(username=username)).scalar()

            # return jsonify({"message": check_password_hash(user.password,password)})

            if user is not None and check_password_hash(user.password, password):

                login_user(user)
                
                return jsonify({"message": "Login Successfull","user_id": user.id, "username": user.username, "firstname": user.firstname, "lastname": user.lastname, "location": user.location, "biography": user.biography, "photo": user.photo, "joined_on": user.joined_on})
        else:
            return jsonify({"errors": form_errors(form)})
        
@app.route('/api/v1/auth/logout', methods=['POST'])
@requires_auth
def logout():
    logout_user()
    return jsonify({"message": "Logout Successfull"})

@app.route('/api/users/<user_id>/posts', methods =['POST','GET'])
@requires_auth
def add_post(user_id):
    form =  PostsForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            user_id = user_id

            photo = form.photo.data
            caption = form.caption.data
            
            filename = secure_filename(photo.filename)
            
            new_post = Posts(user_id=user_id, photo=filename, caption=caption) 
            db.session.add(new_post)
            db.session.commit()
            
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return jsonify({"message":"New Post Successfully created!"})
        else:
            return jsonify(errors=form_errors(form))
    elif request.method == 'GET':
        DB = connect_db()

        cur = DB.cursor()

        cur.execute(f"SELECT * from posts where user_id = {user_id}")

        keys = ["id", "user_id", "photo", "caption", "created_on", "u_user_id", "username", "user_photo", "likes"]

        data= cur.fetchall()

        return jsonify({"posts": data})

@app.route('/api/v1/posts', methods=['GET'])
@requires_auth
def show():
    DB = connect_db()

    cur = DB.cursor()
    cur2 = DB.cursor()

    cur.execute(f'SELECT posts.*, users.id, users.username, users.photo, COALESCE(likes.total_likes, 0) AS total_likes FROM posts INNER JOIN users ON posts.user_id = users.id LEFT JOIN (SELECT post_id, COUNT(*) AS total_likes FROM likes GROUP BY post_id) AS likes ON posts.id = likes.post_id;')
    # cur2.execute(f'select id, username from users')
    cur2.execute(f'SELECT posts.*, users.id, users.username, users.photo FROM posts INNER JOIN users ON posts.user_id = users.id')

    data= cur.fetchall()
    info= cur2.fetchall()

    keys = ["id", "user_id", "photo", "caption", "created_on", "u_user_id", "username", "user_photo", "likes"]
    result = [dict(zip(keys, values)) for values in data]
    
    print(result)
    return jsonify({"posts": result, "users": data})

@app.route("/api/posts/<post_id>/like", methods=["POST"])
@requires_auth
def likePost(post_id):

    posts = db.session.execute(db.select(Posts).filter_by(id=post_id)).scalar()

    likes = Likes(user_id = current_user.id, post_id = posts.id)
    db.session.add(likes)
    db.session.commit()
    
    return jsonify({"Message": "Like Successfully Added", "Current User ID": current_user.id})

    # post = db.session.query(Posts).filter_by(id=post_id).first()

    # if current_user.is_authenticated():
    #     return jsonify({"Message": "Success"})
    # else:
    #     return jsonify({"Message": "Failure"})

@app.route('/api/users/<user_id>/count', methods =['GET'])
@requires_auth
def user_posts(user_id):
    DB = connect_db()

    cur = DB.cursor()

    cur.execute(f"SELECT COUNT(*) from posts where user_id = {user_id}")

    data= cur.fetchone()

    return jsonify({"posts": data})

@app.route('/api/users/<user_id>', methods =['GET'])
@requires_auth
def userAccount(user_id):
    user = db.session.execute(db.select(Users).filter_by(id=user_id)).scalar()

    if user is not None:
        return jsonify({"message": "Successfull","user_id": user.id, "username": user.username, "firstname": user.firstname, "lastname": user.lastname, "location": user.location, "biography": user.biography, "photo": user.photo, "joined_on": user.joined_on})

@app.route("/api/users/<user_id>/follow", methods=["POST"])
@requires_auth
def follow(user_id):

    follows = Follows(user_id = user_id, follower_id = current_user.id)
    db.session.add(follows)
    db.session.commit()
    return jsonify({"user": user_id, "current_user": current_user.id})

@app.route("/api/users/<user_id>/follow/check", methods=["GET"])
@requires_auth
def follow_check(user_id):

    DB = connect_db()

    cur = DB.cursor()

    cur.execute(f"SELECT * FROM follows WHERE user_id = {user_id} AND follower_id = {current_user.id}")

    result = cur.fetchall()

    # final = [dict(zip(keys, values)) for values in result]

    if result:
        return jsonify({"Message": "Success"})
    else:
        return jsonify({"Message": "Failure"})

@app.route('/api/users/<user_id>/follower/count', methods =['GET'])
@requires_auth
def follows_count(user_id):
    DB = connect_db()

    cur = DB.cursor()

    cur.execute(f"SELECT COUNT(*) from follows where user_id = {user_id}")

    data= cur.fetchone()

    return jsonify({"follows": data})
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

def connect_db():
    return psycopg2.connect(host="localhost", database="project2", user="project2", password="Wewillpass2023")

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(Users).filter_by(id=id)).scalar()

@app.route("/api/v1/generate-token")
def generate_token():
    timestamp = datetime.utcnow()
    payload = {
        "sub": 1,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=3)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify(token=token)