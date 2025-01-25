from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import EventLog
from datetime import datetime, timedelta
from flask import request

class EventLogResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        archived = bool(int(request.args.get('archived', 0)))
        now = datetime.now()
        
        if archived:
            # Logs archived more than 2 hours ago
            logs = EventLog.query.filter_by(user_id=user_id).filter(
                EventLog.archived_at.isnot(None),
                EventLog.timestamp < now - timedelta(hours=2)
            ).all()
        else:
            # Active logs (within 2 hours)
            logs = EventLog.query.filter_by(user_id=user_id).filter(
                EventLog.archived_at.is_(None),
                EventLog.timestamp >= now - timedelta(hours=2)
            ).all()
        
        return [log.to_dict() for log in logs], 200