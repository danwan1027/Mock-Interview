from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..models import firebase_func as db

import matplotlib
import matplotlib.pyplot as plt
import io
import base64

# Ensure Matplotlib uses a non-interactive backend to avoid GUI errors
matplotlib.use('Agg')

home_view = Blueprint('home_view', __name__)

@home_view.route('/admin')
@login_required
def admin():
    student_list = db.getAllStudent()
    teacher_list = db.getAllTeacher()
    return render_template('adminDashboard.html', student_list=student_list, teacher_list=teacher_list)

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
    scores = []
    department_count = {}

    # Process interview history and collect data
    for interview in interview_history:
        feedback_list = db.getFeedBack(interview['interview_id'])
        if isinstance(feedback_list, list):
            for feedback in feedback_list:
                if isinstance(feedback, dict) and 'rating' in feedback:
                    scores.append(int(feedback['rating']))
                else:
                    print(f"Unexpected feedback format: {feedback}")
        else:
            print(f"Unexpected feedback format: {feedback_list}")
            
        department = interview['department']
        if department in department_count:
            department_count[department] += 1
        else:
            department_count[department] = 1

    # Plot interview scores
    line_graph_url = create_line_graph(scores)
    bar_graph_url = create_bar_graph(department_count)

    return render_template('dashboard/dashboard.html', 
                           current_user=current_user, 
                           interview_history=interview_history,
                           line_graph_url='data:image/png;base64,{}'.format(line_graph_url),
                           bar_graph_url='data:image/png;base64,{}'.format(bar_graph_url))


def create_line_graph(scores):
    x = list(range(1, len(scores) + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(x, scores, marker='o')
    plt.xlabel('Interview')
    plt.ylabel('Score')
    plt.title('Interview Scores Over Time')
    plt.xticks(rotation=45)
    plt.xticks(x)
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    line_graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return line_graph_url


def create_bar_graph(department_count):
    # Create department bar chart
    departments = list(department_count.keys())
    counts = list(department_count.values())

    plt.figure(figsize=(10, 6))
    plt.bar(departments, counts, color='blue')
    plt.xlabel('Department')
    plt.ylabel('Number of Interviews')
    plt.title('Number of Interviews by Department')
    plt.xticks(rotation=45)
    plt.gca().set_xticks(departments)
    plt.gca().set_xticklabels(departments, rotation=45, ha='right')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    bar_graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return bar_graph_url


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
