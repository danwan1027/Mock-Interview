from flask import Blueprint, jsonify, render_template
from ..models import firebase_func as db

stat_view = Blueprint('stat_view', __name__)

@stat_view.route('/average_score')
def average_score(user_id):
    scores = db.db.collection('Feedback').where('user_id', '==', user_id).stream()
    total_score = 0
    count = 0
    
    for record in scores:
        record_data = record.to_dict()
        total_score += record_data.get('user_score', 0)
        count += 1
    
    if count == 0:
        average = 0
    else:
        average = total_score / count
        
    return jsonify({
        'user_id': user_id,
        'average_score': average
    })


@stat_view.route('/pr')
def pr(user_id):
    scores = db.db.collection('Feedback').where('user_id', '==', user_id).stream()
    total_score = 0
    count = 0
    
    for record in scores:
        record_data = record.to_dict()
        total_score += record_data.get('user_score', 0)
        count += 1
    
    if count == 0:
        average = 0
    else:
        average = total_score / count
        
    user_score = average
    
    # 計算這個使用者的平均負數在所有feedback中的pr值
    pr = 0
    scores = db.db.collection('Feedback').stream()
    total_score = 0
    count = 0
    
    for record in scores:
        record_data = record.to_dict()
        total_score += record_data.get('user_score', 0)
        count += 1
        
    if count == 0:
        average = 0
    else:
        average = total_score / count
        
    total_score = average
    
    if total_score == 0:
        pr = 0
    else:
        pr = user_score / total_score
        
    return jsonify({
        'user_id': user_id,
        'pr': pr
    })
    
    
@stat_view.route('/interview_times')
def interview_times(user_id):
    interviews = db.collection('interview').where('user_id', '==', user_id).stream()
    count = 0
    
    for record in interviews:
        count += 1
        
    return jsonify({
        'user_id': user_id,
        'interview_times': count
    })
        