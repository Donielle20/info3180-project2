"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
import os
from flask_login import current_user
from app.models import Follows, Users


###
# Routing for your application.
###

# following a target user #
@app.route("/api/users/<user_id>/follow", methods=["POST"])
@requires_auth
def follow(user_id):
    current_user = Users.query.filter_by(id=user_id).first()
    if(not current_user):
        return jsonify({
            "error": "Oops looks like user does not exist"
        })
    
    data = request.get_json()
    print(data)
    target_id = data['follow_id']
    print(target_id)
    targetuser = Users.query.filter_by(id=target_id).first()

    follow = Follows(follower=targetuser, current_user=current_user)
    db.session.add(follow)
    db.session.commit()

    return jsonify({
        "message": "You are now following " + targetuser.username
    })

# number of followers #
@app.route("/api/users/<user_id>/follow", methods=["GET"])
@requires_auth
def followers(user_id):
    current_user = Users.query.filter_by(id=user_id).first()

    if(not current_user):
        return jsonify({
            "error": "Oops looks like user does not exist"
        })
    
    return jsonify({
        "followers": len(current_user.following)
    })


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


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