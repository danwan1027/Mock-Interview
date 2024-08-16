from ..models import firebase_func as db
from flask import Blueprint, render_template

frontend_redesign_router = Blueprint('frontend_redesign_router', __name__)

@frontend_redesign_router.route('/adminDashboard')
def admim_dashboard():
    students = db.getAllStudent()
    teachers = db.getAllTeacher()
    return render_template('adminDashboard.html', students=students, teachers=teachers)



@frontend_redesign_router.route('/interviewReview')
def interviewReview():
    name = "陳睿弘"
    interview_school = "成功大學"
    interview_department = "航太系"
    overall_grade = 79
    
    eye_contact_review = "你控制了語速，保持了自然的語調，這使得整個對話非常順暢。"
    reply_content_review = "保持簡潔和具體: 在回答問題時，能夠保持簡潔明了。"
    facial_expression_review = "你控制了語速，保持了自然的語調。"
    
    eye_contact_grade = 85
    reply_content_grade = 78
    facial_expression_grade = 50

    return render_template('interviewReview.html',
                           name=name,
                           interview_school=interview_school,
                           interview_department=interview_department,
                           eye_contact_review=eye_contact_review,
                           reply_content_review=reply_content_review,
                           facial_expression_review=facial_expression_review,
                           overall_grade=overall_grade,
                           eye_contact_grade=eye_contact_grade,
                           reply_content_grade=reply_content_grade,
                           facial_expression_grade=facial_expression_grade)

