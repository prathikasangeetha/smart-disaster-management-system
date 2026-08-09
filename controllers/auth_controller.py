from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from models import db
from models.user import User

class AuthController:
    @staticmethod
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            full_name = request.form.get('full_name', '').strip()
            phone = request.form.get('phone', '').strip()

            if not username or not email or not password or not full_name:
                flash('Please fill in all required fields.', 'danger')
                return render_template('register.html')

            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('register.html')

            if User.query.filter_by(username=username).first():
                flash('Username is already taken.', 'danger')
                return render_template('register.html')

            if User.query.filter_by(email=email).first():
                flash('Email is already registered.', 'danger')
                return render_template('register.html')

            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                role='user'
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))

        return render_template('register.html')

    @staticmethod
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))

        if request.method == 'POST':
            login_id = request.form.get('login_id', '').strip()
            password = request.form.get('password', '')
            remember = True if request.form.get('remember') else False

            # Allow login with username or email
            user = User.query.filter((User.username == login_id) | (User.email == login_id)).first()

            if not user or not user.check_password(password):
                flash('Invalid username/email or password.', 'danger')
                return render_template('login.html')

            login_user(user, remember=remember)
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)

            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.dashboard'))

        return render_template('login.html')

    @staticmethod
    def logout():
        logout_user()
        flash('You have been logged out successfully.', 'info')
        return redirect(url_for('main.index'))

    @staticmethod
    def profile():
        if request.method == 'POST':
            full_name = request.form.get('full_name', '').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip().lower()
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')

            if email != current_user.email:
                existing = User.query.filter_by(email=email).first()
                if existing:
                    flash('Email address is already in use by another account.', 'danger')
                    return render_template('profile.html', user=current_user)
                current_user.email = email

            current_user.full_name = full_name
            current_user.phone = phone

            if new_password:
                if not current_password or not current_user.check_password(current_password):
                    flash('Incorrect current password.', 'danger')
                    return render_template('profile.html', user=current_user)
                current_user.set_password(new_password)
                flash('Password updated successfully.', 'success')

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth.profile'))

        user_reports = current_user.reports
        return render_template('profile.html', user=current_user, reports=user_reports)
