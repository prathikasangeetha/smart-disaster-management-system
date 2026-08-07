import os
import sys
from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User
from utils.seed_data import seed_database
from sqlalchemy import create_engine

def get_working_database_uri(config_obj):
    mysql_uri = config_obj.DEFAULT_MYSQL_URI
    env_uri = os.environ.get('DATABASE_URL') or os.environ.get('MYSQL_URI')
    
    target_uri = env_uri or mysql_uri
    if target_uri.startswith('mysql'):
        try:
            # Test MySQL connection
            test_engine = create_engine(target_uri, connect_args={'connect_timeout': 2})
            conn = test_engine.connect()
            conn.close()
            test_engine.dispose()
            return target_uri
        except Exception as e:
            print(f"[Notice] MySQL server unavailable or credentials not set ({e}).")
            print("[Notice] Automatically utilizing local SQLite database for seamless out-of-the-box execution.")
    
    # Fallback SQLite DB
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'disaster_management.db')
    return f"sqlite:///{db_path}"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Cleanly determine DB URI before initializing SQLAlchemy extension
    app.config['SQLALCHEMY_DATABASE_URI'] = get_working_database_uri(Config)

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize SQLAlchemy database
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.report_routes import report_bp
    from routes.shelter_routes import shelter_bp
    from routes.alert_routes import alert_bp
    from routes.guideline_routes import guideline_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(shelter_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(guideline_bp)
    app.register_blueprint(admin_bp)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # Auto-initialize database tables & seed default data
    with app.app_context():
        db.create_all()
        seed_database()

    return app

app = create_app()

if __name__ == '__main__':
    print("==========================================================================")
    print(" Smart Disaster Management and Alert System - Server Starting...")
    print(" Access Web Portal at: http://127.0.0.1:5000/")
    print(" Default Admin Account: admin / admin123")
    print(" Default User Account:  johndoe / user123")
    print("==========================================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
