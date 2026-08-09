from functools import wraps
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.admin_controller import AdminController

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied: Administrator privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    return AdminController.dashboard()

@admin_bp.route('/users')
@admin_required
def users():
    return AdminController.manage_users()

@admin_bp.route('/users/toggle-role/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user_role(user_id):
    return AdminController.toggle_user_role(user_id)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    return AdminController.delete_user(user_id)

@admin_bp.route('/reports')
@admin_required
def reports():
    return AdminController.manage_reports()

@admin_bp.route('/reports/update-status/<int:report_id>', methods=['POST'])
@admin_required
def update_report_status(report_id):
    return AdminController.update_report_status(report_id)

@admin_bp.route('/reports/delete/<int:report_id>', methods=['POST'])
@admin_required
def delete_report(report_id):
    return AdminController.delete_report(report_id)

@admin_bp.route('/shelters', methods=['GET', 'POST'])
@admin_required
def shelters():
    return AdminController.manage_shelters()

@admin_bp.route('/shelters/update/<int:shelter_id>', methods=['POST'])
@admin_required
def update_shelter(shelter_id):
    return AdminController.update_shelter(shelter_id)

@admin_bp.route('/shelters/delete/<int:shelter_id>', methods=['POST'])
@admin_required
def delete_shelter(shelter_id):
    return AdminController.delete_shelter(shelter_id)

@admin_bp.route('/alerts', methods=['GET', 'POST'])
@admin_required
def alerts():
    return AdminController.manage_alerts()

@admin_bp.route('/alerts/toggle/<int:alert_id>', methods=['POST'])
@admin_required
def toggle_alert(alert_id):
    return AdminController.toggle_alert(alert_id)

@admin_bp.route('/alerts/delete/<int:alert_id>', methods=['POST'])
@admin_required
def delete_alert(alert_id):
    return AdminController.delete_alert(alert_id)
