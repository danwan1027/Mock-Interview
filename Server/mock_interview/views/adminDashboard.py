from flask import Blueprint, render_template

adminDashboard = Blueprint('adminDashboard', __name__)

@adminDashboard.route('/adminDashboard')
def admim_dashboard():
    students = [
        {"name": "Jerome Bell", "department": "NCU", "email": "jerome@google.com"},
        {"name": "Floyd Miles", "department": "NTU", "email": "floyd@yahoo.com"},
        {"name": "Floyd Miles", "department": "NTU", "email": "floyd@yahoo.com"},
        {"name": "Floyd Miles", "department": "NTU", "email": "floyd@yahoo.com"},
        {"name": "Floyd Miles", "department": "NTU", "email": "floyd@yahoo.com"},
        {"name": "Floyd Miles", "department": "NTU", "email": "floyd@yahoo.com"}
    ]
    teachers = [
        {"name": "Jerome Bell", "department": "NCU", "email": "jerome@google.com"},
        {"name": "Floyd Miles", "department": "NTU", "email": "floyd@yahoo.com"},
        {"name": "Floyd Miles", "department": "NTU", "email": "floyd@yahoo.com"},
        {"name": "Floyd Miles", "department": "NTU", "email": "floyd@yahoo.com"}
    ]
    return render_template('adminDashboard.html', students=students, teachers=teachers)

