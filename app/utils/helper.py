def format_event_log(log):
    return {
        'id': log.id,
        'trigger_id': log.trigger_id,
        'type': log.type,
        'timestamp': log.timestamp,
        'details': log.details
    }
