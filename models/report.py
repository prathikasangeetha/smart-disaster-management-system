from datetime import datetime
from models import db

class DisasterReport(db.Model):
    __tablename__ = 'disaster_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    disaster_type = db.Column(db.String(50), nullable=False) # Flood, Cyclone, Earthquake, Fire, Landslide, Tsunami, Drought, Other
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    severity = db.Column(db.String(20), nullable=False) # Low, Medium, High
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, Active, Resolved
    risk_level = db.Column(db.String(20), default='MODERATE') # CRITICAL, HIGH, MODERATE, LOW
    safety_recommendation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DisasterReport {self.disaster_type} - {self.location} ({self.status})>'
