from datetime import datetime, timezone
from random import randrange
from uuid import uuid4

from fastapi import FastAPI

from database import insert_and_assert
from fib import fibonacci
from log import get_logger

MIN_UPPER_LIMIT = 450

logger = get_logger(__name__)
app = FastAPI()


class Borg:
    __monostate = None

    def __init__(self):
        if not Borg.__monostate:
            Borg.__monostate = self.__dict__
            self.numbers = set()
        else:
            self.__dict__ = Borg.__monostate


Calculated = Borg()


@app.get("/fibonacci")
def get_random_fibonacci():
    rand_integer = (
        randrange(MIN_UPPER_LIMIT + max(Calculated.numbers)) if Calculated.numbers
        else randrange(MIN_UPPER_LIMIT)
    )

    logger.info(f"Calculating fibonacci for number {rand_integer}")
    random_fibonacci = fibonacci(rand_integer)
    logger.info(f"Fibonacci for {rand_integer} is {random_fibonacci}")

    Calculated.numbers.add(rand_integer)

    _id = uuid4().hex
    utc_timestamp = datetime.now(
        timezone.utc
    ).replace(
        tzinfo=timezone.utc
    ).timestamp()

    data = {
        "id": _id,
        "number": rand_integer,
        "fibonacci": str(random_fibonacci),
        "timestamp": str(utc_timestamp)
    }

    try:
        success = insert_and_assert(data)
    except Exception as exc:
        success = False
        logger.info(f"Failed to insert and assert with exception. Got {exc}")
    finally:
        logger.info(f"Performed db insertion {'with' if success else 'without'} success.")

    return data
