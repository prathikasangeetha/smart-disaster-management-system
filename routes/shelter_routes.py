from flask import Blueprint
from controllers.shelter_controller import ShelterController

shelter_bp = Blueprint('shelter', __name__)

@shelter_bp.route('/shelters')
def shelters():
    return ShelterController.list_shelters()
