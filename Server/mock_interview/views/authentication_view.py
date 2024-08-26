from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import login_form, register_form
from ..models import firebase_func as db

authentication_view = Blueprint('authentication_view', __name__)

@authentication_view.route('/login', methods=['GET', 'POST'])
def login():
    login = login_form.LoginForm()
    admin_register = register_form.AdminRegistrationForm()
    teacher_register = register_form.TeacherRegistrationForm()
    student_register = register_form.StudentRegistrationForm()
    login_error = False
    if request.method == 'POST':
        user = db.get_user_by_email(login.email.data)
        if user and user.check_password(login.password.data):
            login_user(user, login.remember_me.data)
            # return redirect(url_for('home_view.index'))
            if user.role == 'admin':
                return redirect(url_for('home_view.admin'))
            elif user.role == 'teacher':
                return redirect(url_for('interviewer_view.dashboard'))
            else:
                return redirect(url_for('frontend_redesign_router.student_dashboard'))

            return redirect(url_for('home_view.index'))
        else:
            login_error = True
            
    return render_template('authentication/authentication.html',
                                login_form=login,
                                admin_form=admin_register,
                                teacher_form=teacher_register,
                                student_form=student_register,
                                login_error=login_error)

@authentication_view.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_view.index'))

@authentication_view.route('/admin_register', methods=['POST'])
def admin_register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = 'admin'
    profile_image = request.files['profile_image']
    db.addUser(username, password, email, role, profile_image)
    return "success"

@authentication_view.route('/teacher_register', methods=['POST'])
def teacher_register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = 'teacher'
    profile_image = request.files['profile_image']
    school = request.form['school']
    db.addUser(username, password, email, role, profile_image, school=school)
    return "success"

@authentication_view.route('/student_register', methods=['POST'])
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