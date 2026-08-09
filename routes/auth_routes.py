from flask import Blueprint
from flask_login import login_required
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return AuthController.register()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return AuthController.login()

@auth_bp.route('/logout')
def logout():
    return AuthController.logout()

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return AuthController.profile()
