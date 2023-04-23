"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app,db
from flask import render_template, request, jsonify, send_file
from flask_login import current_user, login_required
import os
from app.models import Posts, Users
from app.forms import PostsForm


###
# Routing for your application.
###

@app.route('/api/users/<user_id>', methods =['GET'])
@login_required
def ViewProfile(user_id):
    user = db.session.query(Users).filter_by(id=user_id).first()
    following = current_user.id in [follower.follower_id for follower in user.followers]
    
    currProfile = {"id": user.id, "username":user.usermame, "firstname":user.first_name,
                  "email": user.email, "location": user.location, "biography": user.biography,
                  "profile_photo": os.path.join('./uploads', user.profile_photo), "joined":
                    user.joined_on.strftime("%b %Y"), "following": following, "posts":[]}
    
    return jsonify(user=currProfile)

@app.route('/api/users/<user_id>/posts', methods =['POST'])
def add_post(user_id):
    form =  PostsForm()
    
    if form.validate_on_submit():
        uid = form.id.data
        photo = form.photo.data
        cap_tion = form.caption.data
        
        user = db.session.query(Posts).filter_by(id=user_id).first()
        
        filename = user.username+secure_filename(photo.filename)
        
        datecreated = str(datetime.date.today())
        
        new_post = Posts(user_id=uid, photo=filename, caption=cap_tion, created_on=datecreated) 
        
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        db.session.add(new_post)
        db.commit()
        
        return jsonify(message="New Post Successfully created!")
    return jsonify(errors=form_errors(form))
    
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