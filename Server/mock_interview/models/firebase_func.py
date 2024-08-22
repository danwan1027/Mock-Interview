import firebase_admin
from firebase_admin import credentials, firestore, storage
from firebase_admin.firestore import SERVER_TIMESTAMP
from instance import config
from typing import List
from .User import User


firebase_config = {
    "type": config.type,
    "project_id": config.project_id,
    "private_key_id": config.private_key_id,
    "private_key": config.private_key,
    "client_email": config.client_email,
    "client_id": config.client_id,
    "auth_uri": config.auth_uri,
    "token_uri": config.token_uri,
    "auth_provider_x509_cert_url": config.auth_provider_x509_cert_url,
    "client_x509_cert_url": config.client_x509_cert_url,
}

cred = credentials.Certificate(firebase_config)

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred, {"storageBucket": config.storage_bucket})

# 初始化firestore
db = firestore.client()
bucket = storage.bucket()

# Users
# 新增user
def addUser(username, password, email, role, profile_image, student_id=None, classroom=None, seat_number=None, school=None, department=None, teacher=None):

    user = db.collection('Users').document()
    created_at = SERVER_TIMESTAMP

    blob = bucket.blob(user.id + '/profile_image.png')
    blob.upload_from_file(profile_image, content_type='image/png')
    blob.make_public()
    profile_image = blob.public_url

    data = {
        'user_id': user.id,
        'username': username,
        'password': password, 
        'email': email,
        'role': role,
        'profile_image': profile_image,
        'created_at': created_at,
    }
    if student_id is not None:
        data['student_id'] = student_id
    if classroom is not None:
        data['classroom'] = classroom
    if seat_number is not None:
        data['seat_number'] = seat_number
    if school is not None:
        data['school'] = school
    if department is not None:
        data['department'] = department
    if teacher is not None:
        data['teacher'] = teacher

    user.set(data)

# 刪除user
def delUser(user_id:str):
    user = db.collection('Users').document(user_id)
    user.delete()

# 更新user
def updateUser(user_id:str, username=None, password=None, email=None, profile_image=None, student_id=None, classroom=None, seat_number=None, school=None, department=None, teacher=None):

    user = db.collection('Users').document(user_id)
    updates = {}

    if username is not None:
        updates['username'] = username
    if password is not None:
        updates['password'] = password
    if email is not None:
        updates['email'] = email
    if student_id is not None:
        updates['student_id'] = student_id
    if classroom is not None:
        updates['classroom'] = classroom
    if seat_number is not None:
        updates['seat_number'] = seat_number
    if school is not None:
        updates['school'] = school
    if department is not None:
        updates['department'] = department
    if teacher is not None:
        updates['teacher'] = teacher
    if profile_image is not None:
        blob = bucket.blob(user.id + '/profile_image.png')
        blob.upload_from_string(profile_image.read(), content_type='image/png')
        blob.make_public()

    if updates:
        user.update(updates)

# 取得user
def get_user_by_email(email: str):
    user_query = db.collection('Users').where('email', '==', email).stream()
    
    for user_doc in user_query:
        user_data = user_doc.to_dict()
        if user_data['role'] == 'admin':
            return User(
                id = user_data['user_id'], 
                email = user_data['email'], 
                name = user_data['username'], 
                password = user_data['password'],
                role = user_data['role'],
                profile_image = user_data['profile_image'],
                created_at = user_data['created_at']
            )
        elif user_data['role'] == 'teacher':
            return User(
                id = user_data['user_id'], 
                email = user_data['email'], 
                name = user_data['username'], 
                password = user_data['password'],
                role = user_data['role'],
                profile_image = user_data['profile_image'],
                created_at = user_data['created_at'],
                school = user_data['school']
            )
        else:
            return User(
                id = user_data['user_id'], 
                email = user_data['email'], 
                name = user_data['username'], 
                password = user_data['password'],
                role = user_data['role'],
                profile_image = user_data['profile_image'],
                created_at = user_data['created_at'],
                school = user_data['school'],
                classroom = user_data['classroom'],
                seat_number = user_data['seat_number'],
                department = user_data['department'],
                teacher = user_data['teacher'],
                student_id = user_data['student_id']
            )
    
    return None

def get_user_by_id(user_id: str):
    user_query = db.collection('Users').where('user_id', '==', user_id).stream()
    
    for user_doc in user_query:
        user_data = user_doc.to_dict()
        if user_data['role'] == 'admin':
            return User(
                id = user_data['user_id'], 
                email = user_data['email'], 
                name = user_data['username'], 
                password = user_data['password'],
                role = user_data['role'],
                profile_image = user_data['profile_image'],
                created_at = user_data['created_at']
            )
        elif user_data['role'] == 'teacher':
            return User(
                id = user_data['user_id'], 
                email = user_data['email'], 
                name = user_data['username'], 
                password = user_data['password'],
                role = user_data['role'],
                profile_image = user_data['profile_image'],
                created_at = user_data['created_at'],
                school = user_data['school']
            )
        else:
            return User(
                id = user_data['user_id'], 
                email = user_data['email'], 
                name = user_data['username'], 
                password = user_data['password'],
                role = user_data['role'],
                profile_image = user_data['profile_image'],
                created_at = user_data['created_at'],
                school = user_data['school'],
                classroom = user_data['classroom'],
                seat_number = user_data['seat_number'],
                department = user_data['department'],
                teacher = user_data['teacher'],
                student_id = user_data['student_id']
            )
    
    return None


# Interviews
# 新增interview
def addInterview(college:str, department:str, duration:int, resume, user_id:str):

    interview = db.collection('Interviews').document()

    created_at = interview_date = updated_at = SERVER_TIMESTAMP

    blob = bucket.blob(user_id + '/' + interview.id + '.pdf')
    blob.upload_from_string(resume.read(), content_type='application/pdf')
    blob.make_public()
    resume = blob.public_url

    interview.set({
        'interview_id': interview.id,
        'college': college, 
        'created_at': created_at,
        'department': department,
        'duration': duration,
        'interview_date': interview_date,
        'resume': resume,
        'updated_at': updated_at, 
        'user_id': user_id,
    })
    
    #新增interview的時候會回傳interview_id
    return interview.id


# 刪除interview
def delInterview(interview_id:str):

    interview_ref = db.collection('Interviews').document(interview_id)
    interview_query = db.collection('Interviews').where('interview_id', '==', interview_id).stream()
    
    for interview in interview_query:
        user_id = interview.to_dict()['user_id']
    blob = bucket.blob(user_id + '/' + interview_id + '.pdf')
    blob.delete()
    
    interview_ref.delete()



# Emotion_Recognition
# 新增Emotion_Recognition
def addEmotionRecognition(emotion:str, emotion_suggestion:str, intensity:str, interview_id:str, 
                          total_emotion_count:int, angry_percent:int, disgust_percent:int, fear_percent:int,
                          happy_percent:int, sad_percent:int, surprise_percent:int, neutral_percent:int):

    emo = db.collection('Emotion_Recognition').document()
    timestamp = SERVER_TIMESTAMP

    emo.set({
        'emotion_id': emo.id,
        "emotion": emotion,
        "emotion_suggestion": emotion_suggestion, 
        "intensity": intensity,
        "interview_id": interview_id,
        "timestamp": timestamp,
        "total_emotion_count": total_emotion_count,
        "angry_percent": angry_percent,
        "disgust_percent": disgust_percent,
        "fear_percent": fear_percent,
        "happy_percent": happy_percent,
        "sad_percent": sad_percent,
        "surprise_percent": surprise_percent,
        "neutral_percent": neutral_percent
    })

# 刪除Emotion_Recognition
def delEmotionRecognition(Emotion_Recognition_id:str):
    emo = db.collection('Emotion_Recognition').document(Emotion_Recognition_id)
    emo.delete()



# Eye_Gaze_Tracking
# 新增Eye_Gaze_Tracking
def addEyeGaze(duration:int, eye_contact:bool, gaze_coordinates:str, gaze_suggestion:str, interview_id:str, percentage_looking_at_camera:int):

    eye_gaze = db.collection('Eye_Gaze_Tracking').document()

    eye_gaze.set({
        'gaze_id': eye_gaze.id,
        "duration": duration,
        "eye_contact": eye_contact, 
        "gaze_coordinates": gaze_coordinates,
        "gaze_suggestion": gaze_suggestion,
        "interview_id": interview_id,
        "percentage_looking_at_camera": percentage_looking_at_camera
    })

# 刪除Eye_Gaze_Tracking
def delEyeGaze(eye_gaze_id:str):
    eye_gaze = db.collection('Eye_Gaze_Tracking').document(eye_gaze_id)
    eye_gaze.delete()



# Feedback
# 新增Feedback
def addFeedback(comments:str, rating:int, interview_id:str, user_id:str):

    feedback = db.collection('Feedback').document()
    created_at = SERVER_TIMESTAMP

    feedback.set({
        'feedback_id': feedback.id,
        "comments": comments,
        "created_at": created_at, 
        "rating": rating,
        "interview_id": interview_id,
        "user_id": user_id,
    })

# 刪除Feedback
def delFeedback(feedback_id:str):
    feedback = db.collection('Feedback').document(feedback_id)
    feedback.delete()



# Question_history
# 新增Question_history
def addQuestionHistory(chatgpt_analysis:str, question_id:str, user_id:str, user_reponse:str, user_score:int, interview_id:int):

    history = db.collection('Question_history').document()
    response_date = SERVER_TIMESTAMP

    history.set({
        'history_id': history.id,
        "chatgpt_analysis": chatgpt_analysis,
        "question_id": question_id, 
        "response_date": response_date,
        "user_id": user_id,
        "user_reponse": user_reponse,
        "user_score": user_score,
        "interview_id": interview_id
    })

# 刪除Question_history
def delQuestionHistory(history_id:str):
    history = db.collection('Question_history').document(history_id)
    history.delete()



# Voice_Transcriptions
# 新增Emotion_Recognition
def addVoiceTranscriptions(speech_speed:List[int], transcript:str, interview_id:str):

    voice = db.collection('Voice_Transcriptions').document()
    timestamp = SERVER_TIMESTAMP

    # blob = bucket.blob(interview_id + '/' + voice.id + '.wav')
    # blob.upload_from_file(audio_file, content_type='audio/wav')
    # blob.make_public()
    # audio = blob.public_url

    voice.set({
        'transcription_id': voice.id,
        # "audio_file": audio,
        "speech_speed": speech_speed, 
        "transcript": transcript,
        "interview_id": interview_id,
        "timestamp": timestamp,
    })

# 刪除Voice_Transcriptions
def delVoiceTranscriptions(transcription_id:str):
    
    voice_ref = db.collection('Voice_Transcriptions').document(transcription_id)
    voice_query = db.collection('Voice_Transcriptions').where('transcription_id', '==', transcription_id).stream()
    
    for interview in voice_query:
        interview_id = interview.to_dict()['interview_id']
    # blob = bucket.blob(interview_id + '/' + transcription_id + '.wav')
    # blob.delete()
    
    voice_ref.delete()



# Questions
# 新增Questions
def addQuestions(question_department:str, question_school:str, history_id:str, question_schooldepartment:str, qusetion_text:str, user_id:str):
    
    question = db.collection('Questions').document()
    question_create_time = SERVER_TIMESTAMP

    question.set({
        'question_id': question.id,
        "history_id": history_id,
        "question_create_time": question_create_time,
        "question_department": question_department, 
        "question_school": question_school,
        "question_schooldepartment": question_schooldepartment,
        "question_text": qusetion_text, 
        "user_id": user_id,
    })
    
    # 新增題目的時候會回傳id
    return question.id

# 刪除Questions
def delQuestions(question_id:str):
    question = db.collection('Questions').document(question_id)
    question.delete()


def getHistory(user_id: str):
    Interview_ref = db.collection('Interviews').where('user_id', '==', user_id).stream()
    interview_history = []
    
    for interview in Interview_ref:
        interview_data = interview.to_dict()
        interview_history.append({
            'interview_id': interview_data['interview_id'],
            'college': interview_data['college'],
            'department': interview_data['department'],
            'duration': interview_data['duration'],
            'interview_date': interview_data['interview_date'],
            'resume': interview_data['resume'],
            'updated_at': interview_data['updated_at'],
            'user_id': interview_data['user_id'],
        })
    
    return interview_history



def getInterview(interview_id: str):
    interview_ref = db.collection('Interviews').where('interview_id', '==', interview_id).stream()
    interview = []
    
    for inter in interview_ref:
        inter_data = inter.to_dict()
        interview.append({
            'interview_id': inter_data['interview_id'],
            'college': inter_data['college'],
            'created_at': inter_data['created_at'],
            'department': inter_data['department'],
            'duration': inter_data['duration'],
            'interview_date': inter_data['interview_date'],
            'resume': inter_data['resume'],
            'updated_at': inter_data['updated_at'],
            'user_id': inter_data['user_id'],
        })
    
    return interview


def getEyeGaze(interview_id: str):
    eye_gaze_ref = db.collection('Eye_Gaze_Tracking').where('interview_id', '==', interview_id).stream()
    eye_gaze = []
    
    for gaze in eye_gaze_ref:
        gaze_data = gaze.to_dict()
        eye_gaze.append({
            'gaze_id': gaze_data['gaze_id'],
            'duration': gaze_data['duration'],
            'eye_contact': gaze_data['eye_contact'],
            'gaze_coordinates': gaze_data['gaze_coordinates'],
            'gaze_suggestion': gaze_data['gaze_suggestion'],
            'interview_id': gaze_data['interview_id'],
            'percentage_looking_at_camera': gaze_data['percentage_looking_at_camera'],
        })
    
    return eye_gaze


def getEmotionRecognition(interview_id: str):
    emotion_recognition_ref = db.collection('Emotion_Recognition').where('interview_id', '==', interview_id).stream()
    emotion_recognition = []
    
    for emo in emotion_recognition_ref:
        emo_data = emo.to_dict()
        emotion_recognition.append({
            'emotion_id': emo_data['emotion_id'],
            'emotion': emo_data['emotion'],
            'emotion_suggestion': emo_data['emotion_suggestion'],
            'intensity': emo_data['intensity'],
            'interview_id': emo_data['interview_id'],
            'timestamp': emo_data['timestamp'],
            'total_emotion_count': emo_data['total_emotion_count'],
            'angry_percent': emo_data['angry_percent'],
            'disgust_percent': emo_data['disgust_percent'],
            'fear_percent': emo_data['fear_percent'],
            'happy_percent': emo_data['happy_percent'],
            'sad_percent': emo_data['sad_percent'],
            'surprise_percent': emo_data['surprise_percent'],
            'neutral_percent': emo_data['neutral_percent'],
        })
    
    return emotion_recognition


def getFeedBack(interview_id: str):
    feedback_ref = db.collection('Feedback').where('interview_id', '==', interview_id).stream()
    feedback = []
    
    for feed in feedback_ref:
        feed_data = feed.to_dict()
        feedback.append({
            'feedback_id': feed_data['feedback_id'],
            'comments': feed_data['comments'],
            'created_at': feed_data['created_at'],
            'rating': feed_data['rating'],
            'interview_id': feed_data['interview_id'],
            'user_id': feed_data['user_id'],
        })
    
    return feedback


def getQuestion(interview_id: str):
    question_ref = db.collection('Questions').where('interview_id', '==', interview_id).stream()
    question = []
    
    for ques in question_ref:
        ques_data = ques.to_dict()
        question.append({
            'question_id': ques_data['question_id'],
            'interview_id': ques_data['interview_id'],
            'question_create_time': ques_data['question_create_time'],
            'question_department': ques_data['question_department'],
            'question_school': ques_data['question_school'],
            'question_schooldepartment': ques_data['question_schooldepartment'],
            'question_text': ques_data['question_text'],
            'user_id': ques_data['user_id'],
        })
    
    return question


# Admin 獲得所有老師的資料
def getAllTeacher():
    user_ref = db.collection('Users').where('role', '==', 'teacher').stream()
    user = []
    
    for u in user_ref:
        u_data = u.to_dict()
        user.append({
            'user_id': u_data['user_id'],
            'username': u_data['username'],
            'email': u_data['email'],
            'role': u_data['role'],
            'profile_image': u_data['profile_image'],
            'created_at': u_data['created_at'],
            'school': u_data['school'],
        })
    
    return user

# Admin 獲得所有學生的資料
def getAllStudent():
    user_ref = db.collection('Users').where('role', '==', 'student').stream()
    user = []
    
    for u in user_ref:
        u_data = u.to_dict()
        user.append({
            'user_id': u_data['user_id'],
            'username': u_data['username'],
            'email': u_data['email'],
            'role': u_data['role'],
            'profile_image': u_data['profile_image'],
            'created_at': u_data['created_at'],
            'school': u_data['school'],
            'classroom': u_data['classroom'],
            'seat_number': u_data['seat_number'],
            'department': u_data['department'],
            'teacher': u_data['teacher'],
            'student_id': u_data['student_id'],
        })
    
    return user

# Teacher獲得所有隸屬於自己的學生的資料
def getStudentByTeacher(teacher: str):
    user_ref = db.collection('Users').where('role', '==', 'student').where('teacher', '==', teacher).stream()
    user = []
    
    for u in user_ref:
        u_data = u.to_dict()
        user.append({
            'user_id': u_data['user_id'],
            'username': u_data['username'],
            'email': u_data['email'],
            'role': u_data['role'],
            'profile_image': u_data['profile_image'],
            'created_at': u_data['created_at'],
            'school': u_data['school'],
            'classroom': u_data['classroom'],
            'seat_number': u_data['seat_number'],
            'department': u_data['department'],
            'teacher': u_data['teacher'],
            'student_id': u_data['student_id'],
        })
    
    return user

def getQuestionBySchoolD(schooldepartment: str):
    question_ref = db.collection('Questions').where('question_schooldepartment', '==', schooldepartment).stream()
    question = []
    
    for ques in question_ref:
        ques_data = ques.to_dict()
        question.append({
            'question_id': ques_data['question_id'],
            'interview_id': ques_data['interview_id'],
            'question_create_time': ques_data['question_create_time'],
            'question_department': ques_data['question_department'],
            'question_school': ques_data['question_school'],
            'question_schooldepartment': ques_data['question_schooldepartment'],
            'question_text': ques_data['question_text'],
            'user_id': ques_data['user_id'],
        })
    
    return question


def getQuestionByDepartment(department: str):
    question_ref = db.collection('Questions').where('question_department', '==', department).stream()
    question = []
    
    for ques in question_ref:
        ques_data = ques.to_dict()
        question.append({
            'question_id': ques_data['question_id'],
            'interview_id': ques_data['interview_id'],
            'question_create_time': ques_data['question_create_time'],
            'question_department': ques_data['question_department'],
            'question_school': ques_data['question_school'],
            'question_schooldepartment': ques_data['question_schooldepartment'],
            'question_text': ques_data['question_text'],
            'user_id': ques_data['user_id'],
        })
    
    return question


def getSingleInterview(interview_id: str):
    interview_ref = db.collection('Interviews').where('interview_id', '==', interview_id).stream()
    interview = []
    
    for inter in interview_ref:
        inter_data = inter.to_dict()
        interview.append({
            'interview_id': inter_data['interview_id'],
            'college': inter_data['college'],
            'created_at': inter_data['created_at'],
            'department': inter_data['department'],
            'duration': inter_data['duration'],
            'interview_date': inter_data['interview_date'],
            'resume': inter_data['resume'],
            'updated_at': inter_data['updated_at'],
            'user_id': inter_data['user_id'],
        })
    
    return interview


# 此次面試的所有問題回答
def getInterviewQuestionHistory(interview_id: str):
    answer_ref = db.collection('Question_history').where('interview_id', '==', interview_id).stream()
    answer = []
    
    for ans in answer_ref:
        ans_data = ans.to_dict()
        answer.append({
            'history_id': ans_data['history_id'],
            'chatgpt_analysis': ans_data['chatgpt_analysis'],
            'question_id': ans_data['question_id'],
            'response_date': ans_data['response_date'],
            'user_id': ans_data['user_id'],
            'user_reponse': ans_data['user_reponse'],
            'user_score': ans_data['user_score'],
            'interview_id': ans_data['interview_id'],
        })
        
    return answer


# 計算所有回答的平均分數
def averageReplyScore(interview_id: str):
    score = []
    for ans in getInterviewQuestionHistory(interview_id):
        score.append(ans['user_score'])
        
    return sum(score) / len(score)


# 換算情緒分析後的得分
def countEmotionScore(interview_id: str):
    emotion_recognition = getEmotionRecognition(interview_id)
    emotion_data = emotion_recognition[0]
    weights = {
        'angry': -0.1,
        'disgust': -0.1,
        'fear': -0.1,
        'happy': 0.5,
        'sad': -0.1,
        'surprise': 0.1,
        'neutral': 0.2
    }
    score = (weights['angry'] * emotion_data['angry_percent'] +
             weights['disgust'] * emotion_data['disgust_percent'] +
             weights['fear'] * emotion_data['fear_percent'] +
             weights['happy'] * emotion_data['happy_percent'] +
             weights['sad'] * emotion_data['sad_percent'] +
             weights['surprise'] * emotion_data['surprise_percent'] +
             weights['neutral'] * emotion_data['neutral_percent'])
    
    
    score = score * 20

    return score


# get all feedback rating
def getFeedbackRating(user_id: str):
    feedback_ref = db.collection('Feedback').where('user_id', '==', user_id).stream()
    feedback = []
    
    for feed in feedback_ref:
        feed_data = feed.to_dict()
        feedback.append({
            'feedback_id': feed_data['feedback_id'],
            'comments': feed_data['comments'],
            'created_at': feed_data['created_at'],
            'rating': feed_data['rating'],
            'interview_id': feed_data['interview_id'],
            'user_id': feed_data['user_id'],
        })
    
    return feedback


# get user all interviews eyes percentage looking at camera
def getUserEye(user_id: str):
    interview_ref = db.collection('Interviews').where('user_id', '==', user_id).stream()
    eye_percentage = []
    
    for inter in interview_ref:
        inter_data = inter.to_dict()
        eye_gaze_ref = db.collection('Eye_Gaze_Tracking').where('interview_id', '==', inter_data['interview_id']).stream()
        
        for gaze in eye_gaze_ref:
            gaze_data = gaze.to_dict()
            eye_percentage.append({
                'gaze_id': gaze_data['gaze_id'],
                'duration': gaze_data['duration'],
                'eye_contact': gaze_data['eye_contact'],
                'gaze_coordinates': gaze_data['gaze_coordinates'],
                'gaze_suggestion': gaze_data['gaze_suggestion'],
                'interview_id': gaze_data['interview_id'],
                'percentage_looking_at_camera': gaze_data['percentage_looking_at_camera'],
            })
    
    return eye_percentage


# get user all countEmotionScore
def getUserEmotionScore(user_id: str):
    interview_ref = db.collection('Interviews').where('user_id', '==', user_id).stream()
    emotion_score = []
    
    for inter in interview_ref:
        emotion_score.append(countEmotionScore(inter.to_dict()['interview_id']))
    
    return emotion_score