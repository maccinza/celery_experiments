from copy import copy
from pickle import dumps
from random import randrange, shuffle
from timeit import default_timer as timer

from fastapi import FastAPI

from database import insert_and_assert
from sorter import bubble_sort
from utils.helpers import get_uuid
from utils.log import get_logger

LOWER_LIMIT = 50000
UPPER_LIMIT = 100000

logger = get_logger(__name__)
app = FastAPI()


@app.get("/random_sorting")
def get_random_sorting():
    endpoint_start = timer()
    rand_range = randrange(LOWER_LIMIT, UPPER_LIMIT)
    numbers = [num for num in range(1, rand_range + 1)]
    shuffle(numbers)
    array = copy(numbers)

    logger.info(f"Sorting array with {len(numbers)} shuffled numbers")
    bs_start = timer()
    bubble_sort(numbers)
    bs_elapsed_time = timer() - bs_start
    logger.info(
        f"Bubble sort took {bs_elapsed_time: .2f} seconds to sort array with "
        f"size {len(numbers)}"
    )

    _id = get_uuid()
    data = {
        "id": _id,
        "array": array,
        "time_in_sec": f"{bs_elapsed_time: .2f}",
    }

    pickled = {**data}
    pickled.update({"array": dumps(data["array"])})
    try:
        success = insert_and_assert(pickled)
    except Exception as exc:
        success = False
        logger.error(f"Failed to insert and assert with exception. Got {exc}")
    finally:
        logger.info(f"Performed db insertion {'with' if success else 'without'} success.")

    endpoint_elapsed = timer() - endpoint_start
    logger.info(f"Endpoint took {endpoint_elapsed: .2f} seconds to handle request")

    return data
