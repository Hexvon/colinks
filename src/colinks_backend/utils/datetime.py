from datetime import datetime, timezone


def tzutcnow():
    """Creates tz-aware datetime in UTC"""
    return datetime.now(timezone.utc)
