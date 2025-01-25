from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
import logging

db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)

    # Set up API routes
    api = Api(app)

    # Import resources
    from .resources.user_resource import UserRegisterResource, UserLoginResource
    from .resources.event import EventLogResource
    from .resources.scheduled_trigger import TriggerListResource, TriggerResource
    from .resources.api_trigger import APITriggerListResource, APITriggerResource
    from .resources.execute_api import ExecuteTriggerResource

    # Add User routes
    api.add_resource(UserRegisterResource, '/register')
    api.add_resource(UserLoginResource, '/login')

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
    
    with app.app_context():
        # Drop all existing tables
        # Recreate all tables
        db.create_all()
    

    # Start scheduler
    from .tasks.scheduler import start_scheduler
    start_scheduler(app)

    return app