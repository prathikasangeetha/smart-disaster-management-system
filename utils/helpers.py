import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_image(file_storage):
    if not file_storage or file_storage.filename == '':
        return None
    if allowed_file(file_storage.filename):
        filename = secure_filename(file_storage.filename)
        unique_prefix = str(uuid.uuid4())[:8]
        saved_filename = f"{unique_prefix}_{filename}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, saved_filename)
        file_storage.save(file_path)
        return saved_filename
    return None

def calculate_risk_analysis(disaster_type, severity, description=""):
    """
    Risk Analysis Engine: Determines Risk Level and tailored safety recommendations
    based on disaster type, reported severity, and context keywords.
    """
    disaster_type = (disaster_type or '').strip().capitalize()
    severity = (severity or '').strip().capitalize()
    desc_lower = (description or '').lower()

    # Base severity score
    if severity == 'High':
        base_score = 80
    elif severity == 'Medium':
        base_score = 50
    else:
        base_score = 25

    # Contextual keywords weight adjustment
    critical_keywords = ['trapped', 'submerged', 'spreading', 'collapse', 'toxic', 'explosion', 'casualties', 'blocked']
    for kw in critical_keywords:
        if kw in desc_lower:
            base_score += 5

    # Determine risk level category
    if base_score >= 75:
        risk_level = 'CRITICAL'
        badge_class = 'danger'
    elif base_score >= 50:
        risk_level = 'HIGH'
        badge_class = 'warning'
    elif base_score >= 30:
        risk_level = 'MODERATE'
        badge_class = 'info'
    else:
        risk_level = 'LOW'
        badge_class = 'success'

    # Tailored recommendations matrix
    recommendations_matrix = {
        'Flood': {
            'CRITICAL': 'Evacuate immediately to designated relief shelters or higher elevation. Disconnect power mains. Do not drive or wade into moving water.',
            'HIGH': 'Move valuable items to upper floors. Keep emergency kit handy. Monitor local flood warnings closely.',
            'MODERATE': 'Clear local drainage paths. Stay updated with weather forecasts and prepare emergency rations.',
            'LOW': 'Inspect property for water leaks and clear gutter blockages.'
        },
        'Fire': {
            'CRITICAL': 'Evacuate structure immediately! Stay low beneath smoke, cover mouth with damp cloth, and do not use elevators.',
            'HIGH': 'Shut off gas supply valves if safe to do so. Move away from wind direction of smoke plume.',
            'MODERATE': 'Inspect fire extinguishers, ensure emergency routes are unblocked, stay vigilant.',
            'LOW': 'Review family escape plan and test smoke alarms.'
        },
        'Cyclone': {
            'CRITICAL': 'Seek immediate shelter in a windowless interior room or sturdy shelter. Stay inside during the eye of the storm.',
            'HIGH': 'Board up windows, secure loose outdoor objects, charge communication devices.',
            'MODERATE': 'Store 3-day supply of drinking water and non-perishable food.',
            'LOW': 'Monitor meteorological bulletins and inspect roof tiles.'
        },
        'Earthquake': {
            'CRITICAL': 'Expect intense aftershocks. Inspect gas lines for leaks. Do not enter damaged structures.',
            'HIGH': 'Drop, Cover, and Hold On! Stay away from glass windows, unanchored heavy furniture, and power lines.',
            'MODERATE': 'Move to open space clear of buildings and utility poles if outdoors.',
            'LOW': 'Inspect home foundation and secure tall shelf units.'
        },
        'Landslide': {
            'CRITICAL': 'Evacuate path of flow immediately! Be alert for sudden river flow changes and cracking sounds.',
            'HIGH': 'Stay awake during heavy downpours. Avoid river channels and steep ravines.',
            'MODERATE': 'Watch for tilted trees or new cracks in soil/pavement.',
            'LOW': 'Ensure slope drainage systems around property are clear.'
        }
    }

    type_matrix = recommendations_matrix.get(disaster_type, {})
    recommendation = type_matrix.get(risk_level, 
        'Stay alert, follow official emergency authority broadcasts, keep emergency contacts accessible, and assist elderly or vulnerable neighbors if safe to do so.')

    return {
        'risk_level': risk_level,
        'badge_class': badge_class,
        'recommendation': recommendation
    }
