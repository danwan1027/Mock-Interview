from ..models import firebase_func as db
from flask import Blueprint, render_template

adminDashboard = Blueprint('adminDashboard', __name__)

@adminDashboard.route('/adminDashboard')
def admim_dashboard():
    students = db.getAllStudent()
    teachers = db.getAllTeacher()
    return render_template('adminDashboard.html', students=students, teachers=teachers)

