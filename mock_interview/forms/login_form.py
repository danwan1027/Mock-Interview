from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, validators, PasswordField, BooleanField

class LoginForm(FlaskForm):

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField('Password', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('Keep Logged in')

    submit = SubmitField('Log in')