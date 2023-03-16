import time

from celery import Celery
from requests.status_codes import codes

from database import insert_and_assert
from utils.client import get_fibonacci
from utils.helpers import get_uuid
from utils.log import get_logger


logger = get_logger(__name__)
app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')


@app.task(bind=True)
def fibonate(self):
    logger.info(
        f"Started running task {self.request.id}, will be getting a fibonacci number now."
    )

    status_code, response_data = get_fibonacci()
    success = False
    if status_code == codes.OK:
        success = True
    # TODO
    data = {

    }

    return data


@app.task(bind=True)
def summarize(self, result):
    # TODO
    return None
