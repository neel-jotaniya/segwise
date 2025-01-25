from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        api_triggers = APITrigger.query.filter_by(user_id=user_id).all()
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

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        args = api_trigger_parser.parse_args()

        new_api_trigger = APITrigger(
            user_id=user_id,
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
    @jwt_required()
    def delete(self, api_trigger_id):
        user_id = get_jwt_identity()
        api_trigger = APITrigger.query.filter_by(id=api_trigger_id, user_id=user_id).first()
        if not api_trigger:
            return {'message': 'API Trigger not found'}, 404

        db.session.delete(api_trigger)
        db.session.commit()
        return {'message': 'API Trigger deleted'}, 200
