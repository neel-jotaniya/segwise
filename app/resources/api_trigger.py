from flask_restful import Resource, reqparse
# from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import APITrigger
from .. import db


api_trigger_parser = reqparse.RequestParser()
api_trigger_parser.add_argument('name', required=True, help="Name is required.")
api_trigger_parser.add_argument('description', required=False)
api_trigger_parser.add_argument('api_url', required=True, help="API URL is required.")
api_trigger_parser.add_argument('method', required=False, help="HTTP method (e.g., GET, POST).")
api_trigger_parser.add_argument('headers', type=dict, required=False, help="Headers for the API.")
api_trigger_parser.add_argument('api_payload', type=dict, required=False, help="Payload for the API.")


class APITriggerListResource(Resource):
    # @jwt_required()
    def get(self):
        """
        Retrieve all API triggers for the authenticated user.
        ---
        responses:
            200:
                description: List of API triggers.
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: API Trigger ID.
                            name:
                                type: string
                                description: Name of the trigger.
                            description:
                                type: string
                                description: Description of the trigger.
                            api_url:
                                type: string
                                description: URL of the API.
                            method:
                                type: string
                                description: HTTP method used for the API request.
                            headers:
                                type: object
                                description: Headers for the API request.
                            api_payload:
                                type: object
                                description: Payload for the API request.
                            created_at:
                                type: string
                                format: date-time
                                description: Timestamp when the trigger was created.
        security:
            - bearerAuth: []
        """
        # user_id = get_jwt_identity()
        # api_triggers = APITrigger.query.filter_by(user_id=user_id).all()
        api_triggers = APITrigger.query.all()
        return [
            {
                'id': t.id,
                'name': t.name,
                'description': t.description,
                'api_url': t.api_url,
                'method': t.method,
                'headers': t.headers,
                'api_payload': t.api_payload,
                'created_at': t.created_at.isoformat()
            } for t in api_triggers
        ], 200

    # @jwt_required()
    def post(self):
        """
        Create a new API Trigger for the authenticated user.
        ---
        parameters:
            - in: body
              name: api_trigger
              required: true
              schema:
                type: object
                properties:
                    name:
                        type: string
                        description: Name of the API trigger.
                    description:
                        type: string
                        description: Description of the API trigger.
                    api_url:
                        type: string
                        description: URL of the API to be triggered.
                    method:
                        type: string
                        description: HTTP method for the API request (e.g., GET, POST).
                    headers:
                        type: object
                        description: HTTP headers to be sent with the API request.
                    api_payload:
                        type: object
                        description: Payload for the API request.
        responses:
            201:
                description: API trigger successfully created.
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                        trigger_id:
                            type: integer
        security:
            - bearerAuth: []
        """
        # user_id = get_jwt_identity()
        args = api_trigger_parser.parse_args()

        new_api_trigger = APITrigger(
            # user_id=user_id,
            name=args['name'],
            description=args.get('description'),
            api_url=args['api_url'],
            method=args.get('method', 'POST'),
            headers=args.get('headers'),
            api_payload=args.get('api_payload')
        )
        db.session.add(new_api_trigger)
        db.session.commit()
        return {'message': 'API Trigger created', 'trigger_id': new_api_trigger.id}, 201


class APITriggerResource(Resource):
    # @jwt_required()
    def delete(self, api_trigger_id):
        """
        Delete an API Trigger for the authenticated user.
        ---
        parameters:
            - in: path
              name: api_trigger_id
              required: true
              type: integer
              description: ID of the API trigger to delete.
        responses:
            200:
                description: API trigger successfully deleted.
            404:
                description: API trigger not found.
        security:
            - bearerAuth: []
        """
        # user_id = get_jwt_identity()
        # api_trigger = APITrigger.query.filter_by(id=api_trigger_id, user_id=user_id).first()
        api_trigger = APITrigger.query.filter_by(id=api_trigger_id).first()
        
        if not api_trigger:
            return {'message': 'API Trigger not found'}, 404

        db.session.delete(api_trigger)
        db.session.commit()
        return {'message': 'API Trigger deleted'}, 200
