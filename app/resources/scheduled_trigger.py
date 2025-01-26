from flask_restful import Resource, reqparse
# from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import ScheduledTrigger as Trigger
from .. import db
from datetime import datetime

trigger_parser = reqparse.RequestParser()
trigger_parser.add_argument('name', required=True, help="Name is required.")
trigger_parser.add_argument('description', required=False)
trigger_parser.add_argument('interval', required=False, help="Interval is required for recurring triggers.")
trigger_parser.add_argument('schedule_time', type=str, required=False, help="Schedule time (ISO 8601).")


class TriggerListResource(Resource):
    # @jwt_required()
    def get(self):
        """
        Get all triggers for the current user.
        ---
        responses:
            200:
                description: A list of triggers.
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                            name:
                                type: string
                            description:
                                type: string
                            interval:
                                type: string
                            schedule_time:
                                type: string
                            created_at:
                                type: string
        """
        # user_id = get_jwt_identity()
        # triggers = Trigger.query.filter_by(user_id=user_id).all()
        triggers = Trigger.query.all()
        
        return [
            {
                'id': t.id,
                'name': t.name,
                'description': t.description,
                'interval': t.interval,
                'schedule_time': t.schedule_time.isoformat() if t.schedule_time else None,
                'created_at': t.created_at.isoformat()
            } for t in triggers
        ], 200

    # @jwt_required()
    def post(self):
        """
        Create a new trigger.
        ---
        parameters:
            - in: body
              name: body
              required: true
              schema:
                type: object
                required:
                    - name
                properties:
                    name:
                        type: string
                    description:
                        type: string
                    interval:
                        type: string
                    schedule_time:
                        type: string
        responses:
            201:
                description: Trigger created successfully.
            400:
                description: Validation error.
        """
        # user_id = get_jwt_identity()
        args = trigger_parser.parse_args()

        if not args['interval'] and not args['schedule_time']:
            return {'message': "Triggers require either 'interval' or 'schedule_time'."}, 400

        schedule_time = args.get('schedule_time')
        if schedule_time and schedule_time.endswith('Z'):
            schedule_time = schedule_time.replace('Z', '+00:00')

        new_trigger = Trigger(
            # user_id=user_id,
            name=args['name'],
            description=args.get('description'),
            interval=args.get('interval'),
            schedule_time=datetime.fromisoformat(schedule_time) if schedule_time else None
        )
        db.session.add(new_trigger)
        db.session.commit()
        return {'message': 'Trigger created', 'trigger_id': new_trigger.id}, 201


class TriggerResource(Resource):
    # @jwt_required()
    def delete(self, trigger_id):
        """
        Delete a specific trigger.
        ---
        parameters:
            - in: path
              name: trigger_id
              required: true
              type: integer
        responses:
            200:
                description: Trigger deleted successfully.
            404:
                description: Trigger not found.
        """
        # user_id = get_jwt_identity()
        # trigger = Trigger.query.filter_by(id=trigger_id, user_id=user_id).first()
        trigger = Trigger.query.filter_by(id=trigger_id).first()
        
        if not trigger:
            return {'message': 'Trigger not found'}, 404

        db.session.delete(trigger)
        db.session.commit()
        return {'message': 'Trigger deleted'}, 200
