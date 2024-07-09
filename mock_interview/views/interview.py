from flask import Blueprint, render_template

interview = Blueprint('interview', __name__)

@interview.route('/interview')
def index():
    return render_template('interview.html')
