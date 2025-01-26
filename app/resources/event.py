from flask_restful import Resource
# from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import EventLog
from datetime import datetime, timedelta
from flask import request


class EventLogResource(Resource):
    # @jwt_required()
    def get(self):
        """
        Retrieve event logs for the authenticated user.
        ---
        parameters:
            - in: query
              name: archived
              required: false
              type: integer
              enum: [0, 1]
              default: 0
              description: Flag to filter logs. Use `1` for archived logs and `0` for active logs.
        responses:
            200:
                description: List of event logs.
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: Event log ID.
                            user_id:
                                type: integer
                                description: ID of the user associated with the log.
                            trigger_id:
                                type: integer
                                description: ID of the trigger associated with the log.
                            type:
                                type: string
                                description: Type of the event log.
                            timestamp:
                                type: string
                                format: date-time
                                description: Timestamp of the log entry.
                            archived_at:
                                type: string
                                format: date-time
                                description: When the log was archived (null if not archived).
                            details:
                                type: object
                                description: Additional details about the event log.
        security:
            - bearerAuth: []
        """
        # user_id = get_jwt_identity()
        archived = bool(int(request.args.get('archived', 0)))
        now = datetime.now()
        
        if archived:
            # Logs archived more than 2 hours ago
            # logs = EventLog.query.filter_by(user_id=user_id).filter(
            logs = EventLog.query.filter(
                EventLog.archived_at.isnot(None),
                EventLog.timestamp < now - timedelta(hours=2)
            ).all()
        else:
            # Active logs (within 2 hours)
            # logs = EventLog.query.filter_by(user_id=user_id).filter(
            logs = EventLog.query.filter(
            
                EventLog.archived_at.is_(None),
                EventLog.timestamp >= now - timedelta(hours=2)
            ).all()
        
        return [log.to_dict() for log in logs], 200
