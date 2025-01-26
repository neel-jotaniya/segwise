from .. import db
from datetime import datetime

class EventLog(db.Model):
    __tablename__ = 'event_logs'

    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Foreign keys for two different trigger types (API or Scheduled)
    trigger_id = db.Column(db.Integer, nullable=True)
    # scheduled_trigger_id = db.Column(db.Integer, db.ForeignKey('scheduled_triggers.id'), nullable=True)  # For scheduled triggers
    # api_trigger_id = db.Column(db.Integer, db.ForeignKey('api_triggers.id'), nullable=True)  # For API triggers
    
    type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    details = db.Column(db.JSON, nullable=True)
    archived_at = db.Column(db.DateTime, nullable=True)  # New column
    
    def to_dict(self):
        return {
            'id': self.id,
            # 'user_id': self.user_id,
            'trigger_id': self.trigger_id,
            # 'scheduled_trigger_id': self.scheduled_trigger_id,
            # 'api_trigger_id': self.api_trigger_id,
            'type': self.type,
            'timestamp': self.timestamp.isoformat(),
            'details': self.details,
            'archived_at': self.archived_at.isoformat() if self.archived_at else None
        }
