# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PostsForm(FlaskForm):
    caption = TextAreaField('Caption', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Only images allowed!')])
    submit = SubmitField("Submit")