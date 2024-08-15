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