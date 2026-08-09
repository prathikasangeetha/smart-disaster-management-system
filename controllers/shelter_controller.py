from flask import render_template, request
from models.shelter import Shelter

class ShelterController:
    @staticmethod
    def list_shelters():
        search_query = request.args.get('q', '').strip()
        status_filter = request.args.get('status', '').strip()

        query = Shelter.query

        if search_query:
            query = query.filter(
                (Shelter.name.ilike(f'%{search_query}%')) |
                (Shelter.address.ilike(f'%{search_query}%'))
            )

        if status_filter and status_filter != 'All':
            query = query.filter_by(status=status_filter)

        shelters = query.order_by(Shelter.available_space.desc()).all()
        return render_template('shelters.html', shelters=shelters, search_query=search_query, status_filter=status_filter)
