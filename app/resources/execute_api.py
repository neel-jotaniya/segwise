from flask_restful import Resource
# from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import APITrigger, EventLog
from .. import db
from datetime import datetime


class ExecuteTriggerResource(Resource):
    # @jwt_required()
    def post(self, trigger_id):
        """
        Log the execution of a Trigger or APITrigger based on its type.
        ---
        description: |
          This endpoint is used to log the execution details of a specific API trigger identified by `trigger_id`.
          It captures details like the name, HTTP method, URL, headers, and payload of the API trigger
          and logs it in the event logs for auditing and tracking purposes.

        parameters:
          - in: path
            name: trigger_id
            required: true
            type: integer
            description: |
              The unique ID of the API trigger to execute. This ID is used to fetch the trigger details
              from the database and log its execution.

        responses:
          200:
            description: |
              Successfully logged the execution details of the API trigger.
              Returns a message confirming that the trigger has been logged, including the `trigger_id` 
              and the `log_id` of the event log entry.

            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Message confirming the logging of the API trigger.
                trigger_id:
                  type: integer
                  description: ID of the API trigger.
                log_id:
                  type: integer
                  description: ID of the event log entry.
          404:
            description: |
              Trigger not found. This occurs when no trigger with the provided `trigger_id` exists in the database.
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Error message indicating that the trigger was not found.
          500:
            description: |
              Internal server error. This can happen if there is an issue with logging the execution of the trigger
              or interacting with the database.
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Error message describing the failure in logging the trigger.

        security:
          - bearerAuth: []

        """
        # user_id = get_jwt_identity()

        # api_trigger = APITrigger.query.filter_by(id=trigger_id, user_id=user_id).first()
        api_trigger = APITrigger.query.filter_by(id=trigger_id).first()
        
        if api_trigger:
            try:
                # Log the API trigger execution details
                event_log = EventLog(
                    # user_id=user_id,
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
