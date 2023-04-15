"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from app import db
from flask import render_template, request, jsonify, send_file
import os
from .forms import RegisterForm, LoginForm, PostsForm
from app.models import Users
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash
from app import app, db, login_manager
from flask_login import login_user, logout_user, current_user, login_required

###
# Routing for your application.
###

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

            if user is not None and check_password_hash(user.password, password):
                login_user(user)

                return jsonify({"message": "Login Successfull"})
        else:
            return jsonify({"errors": form_errors(form)})
        
@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout Successfull"})

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