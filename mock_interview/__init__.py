from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager, current_user
from functools import wraps
from .models import firebase_func as db
from flask_bootstrap import Bootstrap


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(user_id)



# 檢查role的decorator
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(current_user.role)
            if not current_user.is_authenticated:
                flash("You need to log in to access this page.", "danger")
                return redirect(url_for('login_view.login'))  # 重定向到登錄頁面

            if current_user.role not in allowed_roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('home.index'))  # 重定向到其他頁面（如首頁）
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