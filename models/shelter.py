from datetime import datetime
from models import db

class Shelter(db.Model):
    __tablename__ = 'shelters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_space = db.Column(db.Integer, nullable=False)
    contact_number = db.Column(db.String(30), nullable=False)
    maps_url = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Open') # Open, Full, Maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def occupancy_percentage(self):
        if self.capacity <= 0:
            return 100
        occupied = self.capacity - self.available_space
        return round((occupied / self.capacity) * 100, 1)

    def __repr__(self):
        return f'<Shelter {self.name} ({self.available_space}/{self.capacity})>'
