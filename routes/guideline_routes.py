from flask import Blueprint, render_template, request
from models.guideline import SafetyGuideline

guideline_bp = Blueprint('guideline', __name__)

@guideline_bp.route('/guidelines')
def guidelines():
    selected_type = request.args.get('type', 'Flood').strip()
    all_guidelines = SafetyGuideline.query.all()
    active_guideline = SafetyGuideline.query.filter_by(disaster_type=selected_type).first()

    if not active_guideline and all_guidelines:
        active_guideline = all_guidelines[0]

    return render_template('guidelines.html', 
                           guidelines=all_guidelines, 
                           active_guideline=active_guideline,
                           selected_type=selected_type)
