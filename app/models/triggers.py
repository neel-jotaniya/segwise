from .. import db
from datetime import datetime

class ScheduledTrigger(db.Model):
    __tablename__ = 'scheduled_triggers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    interval = db.Column(db.String(50), nullable=True)  # 'daily', 'weekly', or custom intervals
    schedule_time = db.Column(db.DateTime, nullable=True)  # Optional for one-time triggers
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_execution_time = db.Column(db.DateTime, nullable=True)


class APITrigger(db.Model):
    __tablename__ = 'api_triggers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    api_url = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False, default='POST')
    headers = db.Column(db.JSON, nullable=True)
    api_payload = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
