import requests

from log import get_logger

WEBSERVER_ADDRESS = "http://localhost:8000"
logger = get_logger(__name__)


def get_fibonacci() -> tuple[int, dict]:
    endpoint = f"{WEBSERVER_ADDRESS}/fibonacci"
    data = {}
    try:
        response = requests.get(endpoint)
    except Exception as exc:
        logger.info(f"Failed to get fibonacci. Got {exc}")
    else:
        if response.status_code == requests.status_codes.codes.OK:
            data = response.json()

    return response.status_code, data
