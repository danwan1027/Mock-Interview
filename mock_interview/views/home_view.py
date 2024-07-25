from flask import Blueprint, render_template
from flask_login import login_required, current_user

home_view = Blueprint('home_view', __name__)

@home_view.route('/')
# @login_required
def index():
    # return render_template('error_handle/404.html')
    return render_template('base.html')
    # return render_template('index.html')


@home_view.route('/home')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html', current_user = current_user)