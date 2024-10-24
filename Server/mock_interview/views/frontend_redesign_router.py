import random
from ..models import firebase_func as db
from flask_login import current_user, login_user
from ..models import firebase_func as db
from ..views import rate_advice as ra
from ..forms import register_form
from flask import Blueprint, jsonify, render_template, request

frontend_redesign_router = Blueprint('frontend_redesign_router', __name__)

@frontend_redesign_router.route('/api/hello', methods=['GET'])
def send_question():
    return jsonify(message='question from Flask!(這段來自Server/mock_interview/views/frontend_redesign_router.py)')

@frontend_redesign_router.route('/api/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    result = data['num1'] + data['num2']
    return jsonify(result=result)

@frontend_redesign_router.route('/adminDashboard')
def admin_dashboard():
    student_register = register_form.StudentRegistrationForm()
    teacher_register = register_form.TeacherRegistrationForm()
    students = db.getAllStudent()
    teachers = db.getAllTeacher()
    return render_template('dashboard/adminDashboard.html',
                            student_list=students, 
                            teacher_list=teachers,
                            teacher_form=teacher_register,
                            student_form=student_register)

@frontend_redesign_router.route('/teacherDashboard')
def teacher_dashboard():
    student_register = register_form.StudentRegistrationForm()
    teacher_register = register_form.TeacherRegistrationForm()
    students = db.getStudentByTeacherEmail(current_user.id)
    teachers = db.getAllTeacher()
    return render_template('dashboard/teacherDashboard.html',
                            student_list=students, 
                            teachers=teachers,
                            teacher_form=teacher_register,
                            student_form=student_register)
    
    
@frontend_redesign_router.route('/studentDashboard')
def student_dashboard():
    # if request.args.get('user_id'):
    #     user_id = request.args.get('user_id')
    # else:
    #     if current_user.is_authenticated:
    #         user_id = current_user.id
    user_id = current_user.id
    # Data to be sent to the template
    overview_data = {
        'average': 75,
        'pr_value': 70,
        'practice_count': 8
    }

    interview_records = db.getHistory(user_id)
    # total_avg = db.getFeedbackRating(current_user.id)
    # eye_contact = db.getUserEye(current_user.id)
    # facial_expression = db.getUserEmotionScore(current_user.id)
    
    # Data for the charts
    trend_chart_data = {
        'labels': ['last_7', 'last_6', 'last_5', 'last_4', 'last_3', 'last_2', 'last_1'],
        'datasets': {
            'total_avg': [65, 59, 80, 81, 56, 55, 40],
            'content_quality': [75, 49, 70, 91, 66, 45, 50],
            'facial_expression': [85, 69, 60, 71, 76, 35, 60],
            'eye_contact': [55, 79, 90, 61, 86, 25, 70]
        }
    }

    score_overview_chart_data = {
        'labels': ['總平均', '回答內容', '臉部表情', '眼睛視線'],
        'personal_scores': [40, 35, 20, 40],
        'overall_scores': [20, 30, 25, 15]
    }

    return render_template(
        'dashboard/studentDashboard.html',
        overview_data=overview_data,
        interview_records=interview_records,
        trend_chart_data=trend_chart_data,
        score_overview_chart_data=score_overview_chart_data,
        user_id=user_id
    )



@frontend_redesign_router.route('/interview_questioning')
def interview_questioning():
    question_text = "在面對生成式 AI 的快速發展背景下，您認為為什麼資料分析仍為重要的學習方向，以及學習的優勢是什麼？"
    image_left = "../static/images/bg_coffee.jpeg"
    image_right = "../static/images/bg_coffee.jpeg"
    
    return render_template('interview_questioning.html', question_text=question_text, image_left=image_left, image_right=image_right)





@frontend_redesign_router.route('/interviewReview')
def interviewReview():
    interview_id = request.args.get('interview_id')
    user_id = request.args.get('user_id')
    print('user_id:', user_id)
    user = db.get_user_by_id(user_id)
    login_user(user, True)
    
    interview_list = db.getSingleInterview(interview_id)
    interview = interview_list[0]
    feedback_list = db.getFeedBack(interview_id)
    feedback = feedback_list[0] 
    eyegaze_list = db.getEyeGaze(interview_id)
    eyegaze = eyegaze_list[0]
    emotion_list = db.getEmotionRecognition(interview_id)
    emotion = emotion_list[0]
    # average_score = db.countAverageScore(interview_id)
    average_score = random.randint(60, 100)
    # facial_score = db.countEmotionScore(interview_id)
    facial_score = 100 - emotion['surprise_percent'] - emotion['sad_percent']
    
    # name = current_user.username
    name = current_user.username
    interview_school = interview['college']
    interview_department = interview['department']
    overall_grade = feedback['rating']
    
    eye_contact_review = eyegaze['gaze_suggestion']
    facial_expression_review = emotion['emotion_suggestion']
    reply_content_review = feedback['comments']
    
    eye_contact_grade = eyegaze['percentage_looking_at_camera']
    reply_content_grade = average_score
    facial_expression_grade = facial_score

    angry_percent = emotion['angry_percent']
    disgust_percent = emotion['disgust_percent']
    fear_percent = emotion['fear_percent']
    happy_percent = emotion['happy_percent']
    sad_percent = emotion['sad_percent']
    surprise_percent = emotion['surprise_percent']
    neutral_percent = emotion['neutral_percent']
    
    # get這次面試的題目和回答
    question_list = db.getQuestion(interview_id)
    user_answer_list = db.getInterviewQuestionHistory(interview_id)
    question1 = question_list[0]['question_text']
    question2 = question_list[1]['question_text']
    answer1 = user_answer_list[0]['user_reponse']
    answer2 = user_answer_list[1]['user_reponse']
    
    gpt_answer_analysis = ra.gen_allanswer_advice(question1, question2 ,answer1, answer2)
    
    
    
    return render_template('interviewReview.html',
                           name=name,
                           user_id=user_id,
                           interview_school=interview_school,
                           interview_department=interview_department,
                           eye_contact_review=eye_contact_review,
                           reply_content_review=reply_content_review,
                           facial_expression_review=facial_expression_review,
                           overall_grade=overall_grade,
                           eye_contact_grade=eye_contact_grade,
                           reply_content_grade=reply_content_grade,
                           facial_expression_grade=facial_expression_grade,
                           angry_percent=angry_percent,
                           disgust_percent=disgust_percent,
                           fear_percent=fear_percent,
                           happy_percent=happy_percent,
                           sad_percent=sad_percent,
                           surprise_percent=surprise_percent,
                           neutral_percent=neutral_percent,
                           gpt_answer_analysis=gpt_answer_analysis
                           )

