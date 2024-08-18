from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, validators, PasswordField, BooleanField

class LoginForm(FlaskForm):

    email = EmailField('電子郵件', validators=[
        validators.DataRequired()
    ])

    password = PasswordField('密碼', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('保持登入')

    # back = SubmitField('Back')
    submit = SubmitField('登入')