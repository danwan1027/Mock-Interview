from flask import Blueprint, render_template
from flask_login import login_required

home_view = Blueprint('home_view', __name__)

@home_view.route('/')
# @login_required
def index():
    return render_template('base.html')
    # return render_template('index.html')
