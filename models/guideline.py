from models import db

class SafetyGuideline(db.Model):
    __tablename__ = 'safety_guidelines'

    id = db.Column(db.Integer, primary_key=True)
    disaster_type = db.Column(db.String(50), unique=True, nullable=False)
    before_tips = db.Column(db.Text, nullable=False)
    during_tips = db.Column(db.Text, nullable=False)
    after_tips = db.Column(db.Text, nullable=False)
    first_aid = db.Column(db.Text, nullable=False)
    emergency_kit = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<SafetyGuideline {self.disaster_type}>'
