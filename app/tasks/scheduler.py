import threading
from datetime import datetime, timedelta
import pytz


def run_scheduled_tasks(app):
    """
    Process scheduled triggers within app context.
    """
    from app.models import ScheduledTrigger, EventLog
    from app import db

    with app.app_context():
        now = datetime.now()  # Ensure we are using UTC time
        # Fetch all scheduled triggers
        scheduled_triggers = ScheduledTrigger.query.all()
        print(f"Found {len(scheduled_triggers)} scheduled triggers.")

        for trigger in scheduled_triggers:
            if trigger.interval:
                # Handle recurring triggers
                next_execution_time = calculate_next_execution_time(trigger, now)
                if next_execution_time and now >= next_execution_time:
                    execute_trigger(trigger, now, db)
                    print(f"Recurring trigger {trigger.id} executed.")
            elif trigger.schedule_time:
                # Handle one-time triggers
                if now >= trigger.schedule_time.replace(tzinfo=None):  # Remove timezone info for comparison
                    execute_trigger(trigger, now, db)

                    # Delete the one-time trigger after execution
                    db.session.delete(trigger)
                    print(f"One-time trigger {trigger.id} executed and deleted.")

        db.session.commit()

        # Clean up old logs
        cleanup_old_logs(app)


def execute_trigger(trigger, timestamp, db):
    """
    Execute the specified trigger and log the event.
    """
    from app.models import EventLog

    # Log the execution event
    event_log = EventLog(
        user_id=trigger.user_id,
        trigger_id=trigger.id,
        type='scheduled',
        timestamp=timestamp,
        details={
            'trigger_name': trigger.name,
            'description': trigger.description,
            'interval': trigger.interval or 'one-time'
        }
    )
    db.session.add(event_log)

    # Update the trigger with the new last execution time
    if trigger.interval:
        trigger.last_execution_time = timestamp
        db.session.commit()


def calculate_next_execution_time(trigger, current_time):
    """
    Calculate the next execution time for a recurring trigger.
    """
    # Use last_execution_time or schedule_time as a base for next execution
    last_execution_time = trigger.last_execution_time or trigger.schedule_time

    if trigger.interval == 'daily':
        next_execution_time = last_execution_time + timedelta(days=1)
    elif trigger.interval == 'weekly':
        next_execution_time = last_execution_time + timedelta(weeks=1)
    else:
        try:
            # Custom intervals (e.g., '30' for 30 minutes)
            custom_interval = int(trigger.interval)
            next_execution_time = last_execution_time + timedelta(minutes=custom_interval)
        except ValueError:
            print(f"Invalid custom interval for trigger {trigger.id}.")
            return None
    
    return next_execution_time


def cleanup_old_logs(app):
    """
    Remove old logs based on retention policy.
    """
    from app.models import EventLog
    from app import db

    with app.app_context():
        now = datetime.now(pytz.utc)

        # Mark logs older than 2 hours as archived
        active_log_cutoff = now - timedelta(hours=2)
        archived_count = EventLog.query.filter(
            EventLog.timestamp < active_log_cutoff,
            EventLog.archived_at.is_(None)
        ).update({EventLog.archived_at: now})
        print(f"Archived {archived_count} old logs.")

        # Remove logs older than 48 hours
        total_log_cutoff = now - timedelta(hours=48)
        deleted_count = EventLog.query.filter(
            EventLog.timestamp < total_log_cutoff
        ).delete()
        print(f"Deleted {deleted_count} logs older than 48 hours.")

        db.session.commit()


def start_scheduler(app):
    """
    Start a background thread to run scheduled tasks.
    """
    def run_periodically():
        while True:
            run_scheduled_tasks(app)
            # Sleep for 1 minute (adjust as needed for your use case)
            threading.Event().wait(8)

    # Start scheduler in a daemon thread
    scheduler_thread = threading.Thread(target=run_periodically, daemon=True)
    scheduler_thread.start()
    return scheduler_thread
