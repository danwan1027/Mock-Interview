from flask import Blueprint

# blueprint in views
from .home_view import home_view
from .interview import interview
from .firebase_test_view import firebase_test_view
from .GPT.generate_question import generate
from .GPT.rate_advice import rate
from .login_view import login_view
from .error_handle_view import error_handle_view
from .frontend_redesign_router import frontend_redesign_router
from .stat_view import stat_view
from .interview_process import interview_process

def init_views(app):
    app.register_blueprint(home_view)
    app.register_blueprint(interview)
    app.register_blueprint(firebase_test_view)
    app.register_blueprint(login_view)
    app.register_blueprint(error_handle_view)
    app.register_blueprint(frontend_redesign_router)
    # wstfu blueprint 
    app.register_blueprint(generate)
    app.register_blueprint(rate)
    app.register_blueprint(stat_view)
    app.register_blueprint(interview_process)