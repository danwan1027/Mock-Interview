from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import login_form, register_form
from ..models import firebase_func as db

login_view = Blueprint('login_view', __name__)

@login_view.route('/login', methods=['GET', 'POST'])
def login():
    login = login_form.LoginForm()
    admin_register = register_form.AdminRegistrationForm()
    teacher_register = register_form.TeacherRegistrationForm()
    student_register = register_form.StudentRegistrationForm()
    # if form.validate_on_submit():
    user = db.get_user_by_email(login.email.data)
    if user:
        if user.check_password(login.password.data):
            login_user(user, login.remember_me.data)
            if user.role == 'admin':
                return redirect(url_for('adminDashboard.admim_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('interviewer_view.dashboard'))
            else:
                return redirect(url_for('home_view.dashboard'))
            # return 'Welcome:' + current_user.username + current_user.created_at.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('authentication/authentication.html',
                           login_form=login,
                           admin_form=admin_register,
                           teacher_form=teacher_register,
                           student_form=student_register)

@login_view.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_view.login'))

@login_view.route('/admin_register', methods=['POST'])
def admin_register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = 'admin'
    profile_image = request.files['profile_image']
    db.addUser(username, password, email, role, profile_image)
    return "success"

@login_view.route('/teacher_register', methods=['POST'])
def teacher_register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = 'teacher'
    profile_image = request.files['profile_image']
    school = request.form['school']
    db.addUser(username, password, email, role, profile_image, school=school)
    return "success"

@login_view.route('/student_register', methods=['POST'])
def student_register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = 'student'
    profile_image = request.files['profile_image']
    school = request.form['school']
    student_id = request.form['student_id']
    classroom = request.form['classroom']
    seat_number = request.form['seat_number']
    department = request.form['department']
    teacher = request.form['teacher']
    db.addUser(username, password, email, role, profile_image, student_id, classroom, seat_number, school, department, teacher)
    return "success"