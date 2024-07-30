from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..models import firebase_func as db

home_view = Blueprint('home_view', __name__)

@home_view.route('/')
# @login_required
def index():
    # return render_template('error_handle/404.html')
    return render_template('base.html')
    # return render_template('index.html')


@home_view.route('/home')
@login_required
def dashboard():
    user_id = current_user.id
    interview_history = db.getHistory(user_id)
    return render_template('dashboard/dashboard.html', current_user = current_user, interview_history = interview_history)


@home_view.route('/interview_detail/<interview_id>', methods=['GET'])
@login_required
def interview_detail(interview_id):
    Interview = db.getInterview(interview_id)
    EyeGaze = db.getEyeGaze(interview_id)
    EmotionRecognition = db.getEmotionRecognition(interview_id)
    Feedback = db.getFeedBack(interview_id)
    Question = db.getQuestion(interview_id)
    return render_template('/interview_detail.html', 
                           Interview=Interview,
                           EyeGaze=EyeGaze,
                           EmotionRecognition=EmotionRecognition,
                           Feedback=Feedback,
                           Question=Question)