from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import APITrigger, EventLog
from .. import db
from datetime import datetime


class ExecuteTriggerResource(Resource):
    @jwt_required()
    def post(self, trigger_id):
        """
        Log the execution of a Trigger or APITrigger based on its type.
        """
        user_id = get_jwt_identity()

        api_trigger = APITrigger.query.filter_by(id=trigger_id, user_id=user_id).first()
        if api_trigger:
            try:
                # Log the API trigger execution details
                event_log = EventLog(
                    user_id=user_id,
                    trigger_id=api_trigger.id,
                    type='api_trigger_log',
                    timestamp=datetime.now(),
                    details={
                        'name': api_trigger.name,
                        'method': api_trigger.method,
                        'api_url': api_trigger.api_url,
                        'headers': api_trigger.headers,
                        'payload': api_trigger.api_payload
                    }
                )
                db.session.add(event_log)
                db.session.commit()

                return {
                    'message': f"API Trigger '{api_trigger.name}' logged successfully.",
                    'trigger_id': api_trigger.id,
                    'log_id': event_log.id
                }, 200

            except Exception as e:
                db.session.rollback()  # Ensure database integrity on error
                return {'message': f"Failed to log API Trigger: {str(e)}"}, 500

        # If no trigger is found
        return {'message': 'Trigger not found'}, 404
