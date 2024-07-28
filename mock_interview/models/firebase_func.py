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
def addUser(username, password, email, role, profile_image):

    user = db.collection('Users').document()
    created_at = SERVER_TIMESTAMP

    blob = bucket.blob(user.id + '/profile_image.png')
    blob.upload_from_file(profile_image, content_type='image/png')
    blob.make_public()
    profile_image = blob.public_url

    user.set({
        'user_id': user.id,
        'username': username,
        'password': password, 
        'email': email,
        'role': role,
        'profile_image': profile_image,
        'created_at': created_at
    })

# 刪除user
def delUser(user_id:str):
    user = db.collection('Users').document(user_id)
    user.delete()

# 更新user
def updateUser(user_id:str, username=None, password=None, email=None, profile_image=None):

    user = db.collection('Users').document(user_id)
    updates = {}

    if username is not None:
        updates['username'] = username
    if password is not None:
        updates['password'] = password
    if email is not None:
        updates['email'] = email
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
        return User(
            id = user_data['user_id'], 
            email = user_data['email'], 
            name = user_data['username'], 
            password = user_data['password'],
            role = user_data['role'],
            profile_image = user_data['profile_image'],
            created_at = user_data['created_at']
        )
    
    return None

def get_user_by_id(user_id: str):
    user_query = db.collection('Users').where('user_id', '==', user_id).stream()
    
    for user_doc in user_query:
        user_data = user_doc.to_dict()
        return User(
            id = user_data['user_id'], 
            email = user_data['email'], 
            name = user_data['username'], 
            password = user_data['password'],
            role = user_data['role'],
            profile_image = user_data['profile_image'],
            created_at = user_data['created_at']
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
def addEmotionRecognition(emotion:str, emotion_suggestion:str, intensity:str, interview_id:str):

    emo = db.collection('Emotion_Recognition').document()
    timestamp = SERVER_TIMESTAMP

    emo.set({
        'emotion_id': emo.id,
        "emotion": emotion,
        "emotion_suggestion": emotion_suggestion, 
        "intensity": intensity,
        "interview_id": interview_id,
        "timestamp": timestamp,
    })

# 刪除Emotion_Recognition
def delEmotionRecognition(Emotion_Recognition_id:str):
    emo = db.collection('Emotion_Recognition').document(Emotion_Recognition_id)
    emo.delete()



# Eye_Gaze_Tracking
# 新增Eye_Gaze_Tracking
def addEyeGaze(duration:int, eye_contact:bool, gaze_coordinates:str, gaze_suggestion:str, interview_id:str):

    eye_gaze = db.collection('Eye_Gaze_Tracking').document()

    eye_gaze.set({
        'gaze_id': eye_gaze.id,
        "duration": duration,
        "eye_contact": eye_contact, 
        "gaze_coordinates": gaze_coordinates,
        "gaze_suggestion": gaze_suggestion,
        "interview_id": interview_id,
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
def addQuestionHistory(chatgpt_analysis:str, question_id:str, user_id:str, user_reponse:str, user_score:int):

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
    })

# 刪除Question_history
def delQuestionHistory(history_id:str):
    history = db.collection('Question_history').document(history_id)
    history.delete()



# Voice_Transcriptions
# 新增Emotion_Recognition
def addVoiceTranscriptions(audio_file, speech_speed:List[int], transcript:str, interview_id:str):

    voice = db.collection('Voice_Transcriptions').document()
    timestamp = SERVER_TIMESTAMP

    blob = bucket.blob(interview_id + '/' + voice.id + '.wav')
    blob.upload_from_file(audio_file, content_type='audio/wav')
    blob.make_public()
    audio = blob.public_url

    voice.set({
        'transcription_id': voice.id,
        "audio_file": audio,
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
    blob = bucket.blob(interview_id + '/' + transcription_id + '.wav')
    blob.delete()
    
    voice_ref.delete()



# Questions
# 新增Questions
def addQuestions(question_department:str, question_school:str, interview_id:str, question_schooldepartment:str, qusetion_text:str, user_id:str):
    
    question = db.collection('Questions').document()
    question_create_time = SERVER_TIMESTAMP

    question.set({
        'question_id': question.id,
        "interview_id": interview_id,
        "question_create_time": question_create_time,
        "question_department": question_department, 
        "question_school": question_school,
        "question_schooldepartment": question_schooldepartment,
        "qusetion_text": qusetion_text, 
        "user_id": user_id,
    })
    
    # 新增題目的時候會回傳id
    return question.id

# 刪除Questions
def delQuestions(question_id:str):
    question = db.collection('Questions').document(question_id)
    question.delete()
    