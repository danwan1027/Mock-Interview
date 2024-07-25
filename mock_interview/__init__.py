from flask import Flask, flash, redirect, url_for, abort
from flask_login import LoginManager, current_user
from functools import wraps
from .models import firebase_func as db
from flask_bootstrap import Bootstrap


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = db.get_user_by_id(user_id)
    # print(user.profile_image)
    return user
                           

# 檢查role的decorator
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in allowed_roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # config
    app.config.from_object('config.development')
    # app.config.from_object('config.product')
    app.config.from_pyfile('config.py')

    # bootstrap
    bootstrap = Bootstrap(app)


    # login
    login_manager.init_app(app)
    login_manager.login_view = 'login_view.login'
    
    
    # blueprint
    from .views import init_views
    init_views(app)
    
    return app