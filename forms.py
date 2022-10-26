from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    HiddenField
)
from wtforms.validators import (
    InputRequired,
    Length,
    Email
)


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[
                           InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(max=100)])
    email = StringField("Email", validators=[
                        InputRequired(), Length(max=50), Email()])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[
                           InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(max=100)])


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""


class AddNoteForm(FlaskForm):
    """ Form for adding a new note """

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])
    owner = HiddenField("Username")

class EditNoteForm(FlaskForm):
    """Form for editing an existing note"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()]) #TODO:TextArea
