from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from models import db
from models.user import User
from models.report import DisasterReport
from models.shelter import Shelter
from models.alert import Alert

class AdminController:
    @staticmethod
    def dashboard():
        total_users = User.query.count()
        total_reports = DisasterReport.query.count()
        active_reports = DisasterReport.query.filter_by(status='Active').count()
        resolved_reports = DisasterReport.query.filter_by(status='Resolved').count()
        pending_reports = DisasterReport.query.filter_by(status='Pending').count()
        total_shelters = Shelter.query.count()
        total_alerts = Alert.query.count()

        latest_reports = DisasterReport.query.order_by(DisasterReport.created_at.desc()).limit(5).all()
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

        return render_template('admin/dashboard.html',
                               total_users=total_users,
                               total_reports=total_reports,
                               active_reports=active_reports,
                               resolved_reports=resolved_reports,
                               pending_reports=pending_reports,
                               total_shelters=total_shelters,
                               total_alerts=total_alerts,
                               latest_reports=latest_reports,
                               recent_users=recent_users)

    # ------------------ User Management ------------------
    @staticmethod
    def manage_users():
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template('admin/users.html', users=users)

    @staticmethod
    def toggle_user_role(user_id):
        if user_id == current_user.id:
            flash('You cannot modify your own admin role.', 'warning')
            return redirect(url_for('admin.users'))

        user = User.query.get_or_404(user_id)
        user.role = 'user' if user.role == 'admin' else 'admin'
        db.session.commit()
        flash(f'Updated role for {user.username} to {user.role}.', 'success')
        return redirect(url_for('admin.users'))

    @staticmethod
    def delete_user(user_id):
        if user_id == current_user.id:
            flash('You cannot delete your own admin account.', 'danger')
            return redirect(url_for('admin.users'))

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
        return redirect(url_for('admin.users'))

    # ------------------ Report Management ------------------
    @staticmethod
    def manage_reports():
        reports = DisasterReport.query.order_by(DisasterReport.created_at.desc()).all()
        return render_template('admin/reports.html', reports=reports)

    @staticmethod
    def update_report_status(report_id):
        report = DisasterReport.query.get_or_404(report_id)
        new_status = request.form.get('status', '').strip()

        if new_status in ['Pending', 'Active', 'Resolved']:
            report.status = new_status
            db.session.commit()
            flash(f'Report #{report.id} status updated to {new_status}.', 'success')
        else:
            flash('Invalid status choice.', 'danger')

        return redirect(url_for('admin.reports'))

    @staticmethod
    def delete_report(report_id):
        report = DisasterReport.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        flash('Disaster report deleted successfully.', 'success')
        return redirect(url_for('admin.reports'))

    # ------------------ Shelter Management ------------------
    @staticmethod
    def manage_shelters():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            address = request.form.get('address', '').strip()
            capacity = int(request.form.get('capacity', 0))
            available_space = int(request.form.get('available_space', 0))
            contact_number = request.form.get('contact_number', '').strip()
            maps_url = request.form.get('maps_url', '').strip()
            status = request.form.get('status', 'Open').strip()

            if not name or not address or not contact_number:
                flash('Shelter Name, Address, and Contact Number are required.', 'danger')
            else:
                shelter = Shelter(
                    name=name,
                    address=address,
                    capacity=capacity,
                    available_space=available_space,
                    contact_number=contact_number,
                    maps_url=maps_url,
                    status=status
                )
                db.session.add(shelter)
                db.session.commit()
                flash('New shelter added successfully!', 'success')
                return redirect(url_for('admin.shelters'))

        shelters = Shelter.query.order_by(Shelter.created_at.desc()).all()
        return render_template('admin/shelters.html', shelters=shelters)

    @staticmethod
    def update_shelter(shelter_id):
        shelter = Shelter.query.get_or_404(shelter_id)
        if request.method == 'POST':
            shelter.name = request.form.get('name', shelter.name).strip()
            shelter.address = request.form.get('address', shelter.address).strip()
            shelter.capacity = int(request.form.get('capacity', shelter.capacity))
            shelter.available_space = int(request.form.get('available_space', shelter.available_space))
            shelter.contact_number = request.form.get('contact_number', shelter.contact_number).strip()
            shelter.maps_url = request.form.get('maps_url', shelter.maps_url).strip()
            shelter.status = request.form.get('status', shelter.status).strip()

            db.session.commit()
            flash(f'Shelter "{shelter.name}" updated successfully.', 'success')

        return redirect(url_for('admin.shelters'))

    @staticmethod
    def delete_shelter(shelter_id):
        shelter = Shelter.query.get_or_404(shelter_id)
        db.session.delete(shelter)
        db.session.commit()
        flash('Shelter deleted successfully.', 'success')
        return redirect(url_for('admin.shelters'))

    # ------------------ Alert Management ------------------
    @staticmethod
    def manage_alerts():
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            disaster_type = request.form.get('disaster_type', '').strip()
            affected_area = request.form.get('affected_area', '').strip()
            severity_level = request.form.get('severity_level', 'High').strip()
            description = request.form.get('description', '').strip()
            evacuation_instructions = request.form.get('evacuation_instructions', '').strip()

            if not title or not disaster_type or not affected_area or not description:
                flash('Please complete all required alert fields.', 'danger')
            else:
                alert = Alert(
                    title=title,
                    disaster_type=disaster_type,
                    affected_area=affected_area,
                    severity_level=severity_level,
                    description=description,
                    evacuation_instructions=evacuation_instructions,
                    is_active=True
                )
                db.session.add(alert)
                db.session.commit()
                flash('Emergency broadcast alert created and published!', 'success')
                return redirect(url_for('admin.alerts'))

        alerts = Alert.query.order_by(Alert.created_at.desc()).all()
        return render_template('admin/alerts.html', alerts=alerts)

    @staticmethod
    def toggle_alert(alert_id):
        alert = Alert.query.get_or_404(alert_id)
        alert.is_active = not alert.is_active
        db.session.commit()
        status_str = "activated" if alert.is_active else "deactivated"
        flash(f'Emergency alert "{alert.title}" was {status_str}.', 'info')
        return redirect(url_for('admin.alerts'))

    @staticmethod
    def delete_alert(alert_id):
        alert = Alert.query.get_or_404(alert_id)
        db.session.delete(alert)
        db.session.commit()
        flash('Alert deleted successfully.', 'success')
        return redirect(url_for('admin.alerts'))
