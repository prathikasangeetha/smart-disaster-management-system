from flask import render_template, request
from models.alert import Alert

class AlertController:
    @staticmethod
    def list_alerts():
        search_query = request.args.get('q', '').strip()
        type_filter = request.args.get('type', '').strip()

        query = Alert.query

        if search_query:
            query = query.filter(
                (Alert.title.ilike(f'%{search_query}%')) |
                (Alert.affected_area.ilike(f'%{search_query}%')) |
                (Alert.description.ilike(f'%{search_query}%'))
            )

        if type_filter and type_filter != 'All':
            query = query.filter_by(disaster_type=type_filter)

        alerts = query.order_by(Alert.created_at.desc()).all()
        return render_template('alerts.html', alerts=alerts, search_query=search_query, type_filter=type_filter)
