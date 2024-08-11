from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from ..models import firebase_func as db
from mock_interview import role_required

firebase_test_view = Blueprint('firebase_test_view', __name__)

@firebase_test_view.route('/firebase')
def firebase():
    return render_template('firebase_test.html')

# Route to add a user
@firebase_test_view.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = request.form['role']
    profile_image = request.files['profile_image']
    db.addUser(username, password, email, role, profile_image)
    return jsonify({"message": "User added successfully"}), 200

# Route to update a user
@firebase_test_view.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['user_id']
    username = request.form['username'] if request.form['username'] else None
    password = request.form['password'] if request.form['password'] else None
    email = request.form['email'] if request.form['email'] else None
    profile_image = request.files['profile_image'] if request.files['profile_image'] else None
    db.updateUser(user_id, username, password, email, profile_image)
    return jsonify({"message": "User updated successfully"}), 200

# Route to delete a user
@firebase_test_view.route('/del_user', methods=['POST'])
@role_required(['admin'])
def delete_user():
    user_id = request.form['user_id']
    db.delUser(user_id)
    return jsonify({"message": "User deleted successfully"}), 200

# Route to get user ID by email
@firebase_test_view.route('/get_user_id', methods=['POST'])
def get_user_id():
    email = request.form['email']
    db.getUserID(email)
    return jsonify({"message": "User ID fetched successfully"}), 200

# Route to add an interview
@firebase_test_view.route('/add_interview', methods=['POST'])
def add_interview():
    college = request.form['college']
    department = request.form['department']
    duration = int(request.form['duration'])
    resume = request.files['resume']
    user_id = request.form['user_id']
    filename = secure_filename(resume.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(filepath)
    with open(filepath, 'rb') as f:
        db.addInterview(college, department, duration, f, user_id)
    os.remove(filepath)
    return jsonify({"message": "Interview added successfully"}), 200

# Route to delete an interview
@firebase_test_view.route('/del_interview', methods=['POST'])
def delete_interview():
    interview_id = request.form['interview_id']
    db.delInterview(interview_id)
    return jsonify({"message": "Interview deleted successfully"}), 200

# Route to add an emotion recognition
@firebase_test_view.route('/add_emotion_recognition', methods=['POST'])
def add_emotion_recognition():
    emotion = request.form['emotion']
    emotion_suggestion = request.form['emotion_suggestion']
    intensity = request.form['intensity']
    interview_id = request.form['interview_id']
    db.addEmotionRecognition(emotion, emotion_suggestion, intensity, interview_id)
    return jsonify({"message": "Emotion recognition added successfully"}), 200

# Route to delete an emotion recognition
@firebase_test_view.route('/del_emotion_recognition', methods=['POST'])
def delete_emotion_recognition():
    emotion_recognition_id = request.form['emotion_recognition_id']
    db.delEmotionRecognition(emotion_recognition_id)
    return jsonify({"message": "Emotion recognition deleted successfully"}), 200

# Route to add an eye gaze tracking
@firebase_test_view.route('/add_eye_gaze', methods=['POST'])
def add_eye_gaze():
    duration = int(request.form['duration'])
    eye_contact = request.form['eye_contact']
    gaze_coordinates = request.form['gaze_coordinates']
    gaze_suggestion = request.form['gaze_suggestion']
    interview_id = request.form['interview_id']
    db.addEyeGaze(duration, eye_contact, gaze_coordinates, gaze_suggestion, interview_id)
    return jsonify({"message": "Eye gaze tracking added successfully"}), 200

# Route to delete an eye gaze tracking
@firebase_test_view.route('/del_eye_gaze', methods=['POST'])
def delete_eye_gaze():
    eye_gaze_id = request.form['eye_gaze_id']
    db.delEyeGaze(eye_gaze_id)
    return jsonify({"message": "Eye gaze tracking deleted successfully"}), 200

# Route to add feedback
@firebase_test_view.route('/add_feedback', methods=['POST'])
def add_feedback():
    comments = request.form['comments']
    rating = int(request.form['rating'])
    interview_id = request.form['interview_id']
    user_id = request.form['user_id']
    db.addFeedback(comments, rating, interview_id, user_id)
    return jsonify({"message": "Feedback added successfully"}), 200

# Route to delete feedback
@firebase_test_view.route('/del_feedback', methods=['POST'])
def delete_feedback():
    feedback_id = request.form['feedback_id']
    db.delFeedback(feedback_id)
    return jsonify({"message": "Feedback deleted successfully"}), 200

# Route to add question history
@firebase_test_view.route('/add_question_history', methods=['POST'])
def add_question_history():
    chatgpt_analysis = request.form['chatgpt_analysis']
    question_id = request.form['question_id']
    user_id = request.form['user_id']
    user_reponse = request.form['user_reponse']
    user_score = int(request.form['user_score'])
    db.addQuestionHistory(chatgpt_analysis, question_id, user_id, user_reponse, user_score)
    return jsonify({"message": "Question history added successfully"}), 200

# Route to delete question history
@firebase_test_view.route('/del_question_history', methods=['POST'])
def delete_question_history():
    history_id = request.form['history_id']
    db.delQuestionHistory(history_id)
    return jsonify({"message": "Question history deleted successfully"}), 200

# Route to add voice transcriptions
@firebase_test_view.route('/add_voice_transcriptions', methods=['POST'])
def add_voice_transcriptions():
    audio_file = request.files['audio_file']
    speech_speed_str = request.form['speech_speed']
    speech_speed = [int(speed.strip()) for speed in speech_speed_str.split(',')]
    transcript = request.form['transcript']
    interview_id = request.form['interview_id']
    db.addVoiceTranscriptions(audio_file, speech_speed, transcript, interview_id)
    return jsonify({"message": "Voice transcriptions added successfully"}), 200

# Route to delete voice transcriptions
@firebase_test_view.route('/del_voice_transcriptions', methods=['POST'])
def delete_voice_transcriptions():
    voice_id = request.form['voice_id']
    db.delVoiceTranscriptions(voice_id)
    return jsonify({"message": "Voice transcriptions deleted successfully"}), 200

# Route to add questions
@firebase_test_view.route('/add_questions', methods=['POST'])
def add_questions():
    question_department = request.form['question_department']
    question_school = request.form['question_school']
    interview_id = request.form['interview_id']
    question_schooldepartment = request.form['question_schooldepartment']
    qusetion_text = request.form['qusetion_text']
    user_id = request.form['user_id']
    db.addQuestions(question_department, question_school, interview_id, question_schooldepartment, qusetion_text, user_id)
    return jsonify({"message": "Questions added successfully"}), 200

# Route to delete questions
@firebase_test_view.route('/del_questions', methods=['POST'])
def delete_questions():
    question_id = request.form['question_id']
    db.delQuestions(question_id)
    return jsonify({"message": "Questions deleted successfully"}), 200