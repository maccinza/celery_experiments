from copy import copy
from pickle import dumps
from random import randrange
from time import sleep
from timeit import default_timer as timer

from fastapi import FastAPI

from database import insert_and_assert
from utils.helpers import get_uuid
from utils.log import get_logger

ARRAY_SIZE = 80000
MIN_WAIT_SEC = 180
MAX_WAIT_SEC = 210

logger = get_logger(__name__)
app = FastAPI()


@app.get("/random_waiting")
def get_random_waiting():
    endpoint_start = timer()
    wait_time = randrange(MIN_WAIT_SEC, MAX_WAIT_SEC)

    logger.info(f"Will be waiting for {wait_time} seconds...")
    wt_start = timer()
    sleep(wait_time)
    wt_elapsed_time = timer() - wt_start
    logger.info(
        f"Endpoint has taken {wt_elapsed_time: .2f} seconds so far."
    )

    _id = get_uuid()
    data = {
        "id": _id,
        "await_time_sec": f"{wait_time: .2f}",
        "time_in_sec": f"{wt_elapsed_time: .2f}",
    }

    try:
        success = insert_and_assert(data)
    except Exception as exc:
        success = False
        logger.error(f"Failed to insert and assert with exception. Got {exc}")
    finally:
        logger.info(f"Performed db insertion {'with' if success else 'without'} success.")

    endpoint_elapsed = timer() - endpoint_start
    logger.info(f"Endpoint took {endpoint_elapsed: .2f} seconds to handle request")

    return data
