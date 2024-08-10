from flask import Blueprint, render_template

error_handle_view = Blueprint('error_handle_view', __name__)

@error_handle_view.app_errorhandler(404)
def error_404(error):
    return render_template('error_handle/404.html'), 404

@error_handle_view.app_errorhandler(403)
def error_403(error):
    return render_template('error_handle/403.html'), 403
