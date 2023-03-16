from datetime import datetime, timezone
from uuid import uuid4


def get_uuid():
    return uuid4().hex


def get_utc_timestamp():
    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=timezone.utc
    ).timestamp()
