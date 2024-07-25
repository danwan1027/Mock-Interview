from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import login_form
from ..models import firebase_func as db

login_view = Blueprint('login_view', __name__)

@login_view.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form.LoginForm()
    # if form.validate_on_submit():
    user = db.get_user_by_email(form.email.data)
    if user:
        if user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('home_view.dashboard'))
            # return 'Welcome:' + current_user.username + current_user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            flash('Wrong Email or Password')
    else:
        flash('Wrong Email or Password')
    return render_template('login.html', form=form)

@login_view.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_view.login'))
