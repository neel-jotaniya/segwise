from flask_restful import Resource, reqparse
# from flask_jwt_extended import create_access_token
from ..models import User
from .. import db

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True, help="Username is required.")
user_parser.add_argument('password', required=True, help="Password is required.")


class UserRegisterResource(Resource):
    def post(self):
        """
        Register a new user.
        ---
        parameters:
            - in: body
              name: body
              required: true
              schema:
                type: object
                required:
                    - username
                    - password
                properties:
                    username:
                        type: string
                        description: The username for the new user.
                    password:
                        type: string
                        description: The password for the new user.
        responses:
            201:
                description: User registered successfully.
            400:
                description: Username already exists.
        """
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
        """
        Log in a user and return an access token.
        ---
        parameters:
            - in: body
              name: body
              required: true
              schema:
                type: object
                required:
                    - username
                    - password
                properties:
                    username:
                        type: string
                        description: The username of the user.
                    password:
                        type: string
                        description: The password of the user.
        responses:
            200:
                description: Login successful, access token returned.
                schema:
                    type: object
                    properties:
                        access_token:
                            type: string
                            description: The JWT access token.
            401:
                description: Invalid username or password.
        """
        args = user_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and user.check_password(args['password']):
            # access_token = create_access_token(identity=user.id)
            # return {'access_token': access_token}, 200
             return {'status': "Login Successfully"}, 200
        return {'message': 'Invalid username or password'}, 401
