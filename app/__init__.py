from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS  # Assuming swagger is a Python dict or JSON file
from flasgger import Swagger
# Initialize extensions
db = SQLAlchemy()
cache = Cache()
# jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')
    swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "JWT Example API",
        "description": "This is an example of JWT authentication in Swagger",
        "version": "1.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your JWT token in the format: `Bearer <token>`"
        }
    },
    "security": [
        {
            "BearerAuth": []
        }
    ]
})

    # Initialize extensions
    db.init_app(app)
    cache.init_app(app)
    # jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    api = Api(app)  


    # Import resources
    from .resources.user_resource import UserRegisterResource, UserLoginResource
    from .resources.event import EventLogResource
    from .resources.scheduled_trigger import TriggerListResource, TriggerResource
    from .resources.api_trigger import APITriggerListResource, APITriggerResource
    from .resources.execute_api import ExecuteTriggerResource

    # # Add User routes
    # api.add_resource(UserRegisterResource, '/register')
    # api.add_resource(UserLoginResource, '/login')

    # Add Trigger routes
    api.add_resource(TriggerListResource, '/scheduled')
    api.add_resource(TriggerResource, '/scheduled/<int:trigger_id>')

    # Add APITrigger routes
    api.add_resource(APITriggerListResource, '/api')
    api.add_resource(APITriggerResource, '/api/<int:api_trigger_id>')

    # Add Event Log route
    api.add_resource(EventLogResource, '/events')

    # Add Execute Trigger route
    api.add_resource(ExecuteTriggerResource, '/execute/<int:trigger_id>')

    # Create all database tables
    with app.app_context():
        db.create_all()

    # Start scheduler (if required)
    from .tasks.scheduler import start_scheduler
    start_scheduler(app)

    return app
