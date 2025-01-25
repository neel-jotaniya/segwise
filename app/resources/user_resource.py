from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from ..models import User
from .. import db

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True, help="Username is required.")
user_parser.add_argument('password', required=True, help="Password is required.")

class UserRegisterResource(Resource):
    def post(self):
        args = user_parser.parse_args()
        if User.query.filter_by(username=args['username']).first():
            return {'message': 'Username already exists'}, 400
        
        user = User(username=args['username'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

class UserLoginResource(Resource):
    def post(self):
        args = user_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid username or password'}, 401
