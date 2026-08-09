from flask import Blueprint
from controllers.alert_controller import AlertController

alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/alerts')
def alerts():
    return AlertController.list_alerts()
