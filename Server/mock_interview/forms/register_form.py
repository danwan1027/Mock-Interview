from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

class AdminRegistrationForm(FlaskForm):
    username = StringField('名稱', validators=[DataRequired()])
    email = StringField('電子郵件', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    confirm_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password')])
    profile_image = FileField('大頭貼')
    submit = SubmitField('註冊')

class TeacherRegistrationForm(FlaskForm):
    username = StringField('名稱', validators=[DataRequired()])
    email = StringField('電子郵件', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    confirm_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password')])
    school = StringField('任教學校', validators=[DataRequired()])
    profile_image = FileField('大頭貼')
    submit = SubmitField('註冊')

class StudentRegistrationForm(FlaskForm):
    username = StringField('名稱', validators=[DataRequired()])
    email = StringField('電子郵件', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    confirm_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password')])
    student_id = StringField('學號', validators=[DataRequired()])
    classroom = StringField('班級', validators=[DataRequired()])
    seat_number = StringField('座號', validators=[DataRequired()])
    school = StringField('就讀學校', validators=[DataRequired()])
    department = StringField('科系', validators=[DataRequired()])
    teacher = StringField('老師電子郵件', validators=[DataRequired()])
    profile_image = FileField('大頭貼')
    submit = SubmitField('註冊')