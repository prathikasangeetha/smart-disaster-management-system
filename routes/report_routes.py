from flask import Blueprint
from flask_login import login_required
from controllers.report_controller import ReportController

report_bp = Blueprint('report', __name__)

@report_bp.route('/report', methods=['GET', 'POST'])
@login_required
def create_report():
    return ReportController.create_report()

@report_bp.route('/report/<int:report_id>')
def get_report(report_id):
    return ReportController.get_report(report_id)
