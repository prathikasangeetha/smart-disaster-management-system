from datetime import datetime
from models import db

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    disaster_type = db.Column(db.String(50), nullable=False)
    affected_area = db.Column(db.String(255), nullable=False)
    severity_level = db.Column(db.String(20), nullable=False) # Low, Medium, High, Emergency
    description = db.Column(db.Text, nullable=False)
    evacuation_instructions = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Alert {self.title} - {self.severity_level}>'
