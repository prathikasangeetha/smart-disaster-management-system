from flask import Blueprint, render_template, jsonify
from models.report import DisasterReport
from models.user import User
from models.shelter import Shelter
from models.alert import Alert
from controllers.report_controller import ReportController
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    active_alerts = Alert.query.filter_by(is_active=True).order_by(Alert.created_at.desc()).limit(3).all()
    latest_reports = DisasterReport.query.order_by(DisasterReport.created_at.desc()).limit(6).all()
    
    total_reports = DisasterReport.query.count()
    active_disasters = DisasterReport.query.filter_by(status='Active').count()
    resolved_disasters = DisasterReport.query.filter_by(status='Resolved').count()
    total_shelters = Shelter.query.count()
    
    return render_template('index.html',
                           active_alerts=active_alerts,
                           latest_reports=latest_reports,
                           total_reports=total_reports,
                           active_disasters=active_disasters,
                           resolved_disasters=resolved_disasters,
                           total_shelters=total_shelters)

@main_bp.route('/dashboard')
def dashboard():
    total_reports = DisasterReport.query.count()
    active_disasters = DisasterReport.query.filter_by(status='Active').count()
    resolved_disasters = DisasterReport.query.filter_by(status='Resolved').count()
    total_users = User.query.count()
    
    latest_reports = DisasterReport.query.order_by(DisasterReport.created_at.desc()).limit(8).all()
    
    return render_template('dashboard.html',
                           total_reports=total_reports,
                           active_disasters=active_disasters,
                           resolved_disasters=resolved_disasters,
                           total_users=total_users,
                           latest_reports=latest_reports)

@main_bp.route('/api/dashboard-charts')
def dashboard_charts():
    # Disasters by Type
    type_counts = db_session_type_counts()
    
    # Status Breakdown
    status_counts = db_session_status_counts()
    
    # Severity Breakdown
    severity_counts = db_session_severity_counts()

    return jsonify({
        'by_type': type_counts,
        'by_status': status_counts,
        'by_severity': severity_counts
    })

def db_session_type_counts():
    from models import db
    results = db.session.query(
        DisasterReport.disaster_type, func.count(DisasterReport.id)
    ).group_by(DisasterReport.disaster_type).all()
    return {row[0]: row[1] for row in results}

def db_session_status_counts():
    from models import db
    results = db.session.query(
        DisasterReport.status, func.count(DisasterReport.id)
    ).group_by(DisasterReport.status).all()
    return {row[0]: row[1] for row in results}

def db_session_severity_counts():
    from models import db
    results = db.session.query(
        DisasterReport.severity, func.count(DisasterReport.id)
    ).group_by(DisasterReport.severity).all()
    return {row[0]: row[1] for row in results}

@main_bp.route('/search')
def search():
    reports = ReportController.search_and_filter()
    return render_template('dashboard.html', 
                           filtered_reports=reports,
                           is_search=True,
                           total_reports=DisasterReport.query.count(),
                           active_disasters=DisasterReport.query.filter_by(status='Active').count(),
                           resolved_disasters=DisasterReport.query.filter_by(status='Resolved').count(),
                           total_users=User.query.count())
