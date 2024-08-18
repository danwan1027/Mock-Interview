from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user
from ..models import firebase_func as db

interview_process = Blueprint('interview_process', __name__)

@interview_process.route('/start_interview')
def start_interview():
    user_id = current_user.id
    department = request.form.get('department')
    school = request.form.get('school')
    resume = request.files.get('resume')
    if resume is None:
        return jsonify({'error': 'No resume file provided'}), 400
    
    interview_id = db.addInterview(school, department, 1, resume,user_id)
    return render_template('interview.html', interview_id=interview_id)
    