"""Common utility functions."""
import random
import string
from datetime import datetime, timezone, timedelta


def iso_z(dt: datetime = None) -> str:
    """Return ISO 8601 UTC timestamp."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def random_suffix(length: int = 6) -> str:
    """Generate random alphanumeric suffix."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def future_datetime(hours: int = 1) -> datetime:
    """Get a datetime in the future."""
    return datetime.now(timezone.utc) + timedelta(hours=hours)


def past_datetime(hours: int = 1) -> datetime:
    """Get a datetime in the past."""
    return datetime.now(timezone.utc) - timedelta(hours=hours)
