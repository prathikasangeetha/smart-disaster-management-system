from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from models import db
from models.report import DisasterReport
from utils.helpers import save_uploaded_image, calculate_risk_analysis

class ReportController:
    @staticmethod
    def create_report():
        if request.method == 'POST':
            disaster_type = request.form.get('disaster_type', '').strip()
            location = request.form.get('location', '').strip()
            date_time_str = request.form.get('date_time', '').strip()
            description = request.form.get('description', '').strip()
            severity = request.form.get('severity', '').strip()
            latitude_str = request.form.get('latitude', '').strip()
            longitude_str = request.form.get('longitude', '').strip()
            image_file = request.files.get('image')

            if not disaster_type or not location or not description or not severity:
                flash('Please fill in all required fields.', 'danger')
                return render_template('report.html')

            # Parse date time
            try:
                if date_time_str:
                    date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
                else:
                    date_time = datetime.utcnow()
            except ValueError:
                date_time = datetime.utcnow()

            latitude = float(latitude_str) if latitude_str else None
            longitude = float(longitude_str) if longitude_str else None

            # Handle image upload
            saved_image = save_uploaded_image(image_file) if image_file else None

            # Risk Analysis calculation
            analysis = calculate_risk_analysis(disaster_type, severity, description)

            report = DisasterReport(
                user_id=current_user.id,
                disaster_type=disaster_type,
                location=location,
                latitude=latitude,
                longitude=longitude,
                date_time=date_time,
                description=description,
                image_path=saved_image,
                severity=severity,
                status='Pending',
                risk_level=analysis['risk_level'],
                safety_recommendation=analysis['recommendation']
            )

            db.session.add(report)
            db.session.commit()

            flash('Disaster report submitted successfully! Risk level analyzed: ' + analysis['risk_level'], 'success')
            return redirect(url_for('report.get_report', report_id=report.id))

        return render_template('report.html')

    @staticmethod
    def get_report(report_id):
        report = DisasterReport.query.get_or_404(report_id)
        analysis = calculate_risk_analysis(report.disaster_type, report.severity, report.description)
        return render_template('report_detail.html', report=report, analysis=analysis)

    @staticmethod
    def search_and_filter():
        query = DisasterReport.query

        # Search parameter
        search_query = request.args.get('q', '').strip()
        disaster_type = request.args.get('type', '').strip()
        severity = request.args.get('severity', '').strip()
        status = request.args.get('status', '').strip()
        date_from = request.args.get('date_from', '').strip()

        if search_query:
            query = query.filter(
                (DisasterReport.location.ilike(f'%{search_query}%')) |
                (DisasterReport.description.ilike(f'%{search_query}%'))
            )

        if disaster_type and disaster_type != 'All':
            query = query.filter_by(disaster_type=disaster_type)

        if severity and severity != 'All':
            query = query.filter_by(severity=severity)

        if status and status != 'All':
            query = query.filter_by(status=status)

        if date_from:
            try:
                df = datetime.strptime(date_from, '%Y-%m-%d')
                query = query.filter(DisasterReport.date_time >= df)
            except ValueError:
                pass

        reports = query.order_by(DisasterReport.created_at.desc()).all()
        return reports
