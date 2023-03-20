from celery import chord

from sortinator.tasks import sortinate, summarize
from utils.helpers import get_utc_timestamp
from utils.log import get_logger

from settings import NUM_TASKS

logger = get_logger(__name__)


def produce():
    logger.info(f"Starting to produce chords for both queues")
    start = get_utc_timestamp()

    first_queue_tasks = []
    # second_queue_tasks = []
    for _ in range(NUM_TASKS):
        first_queue_tasks.append(
            sortinate.s().set(queue="first_testing")
        )
    # for _ in range(NUM_TASKS//2):
    #     second_queue_tasks.append(
    #         sortinate.s().set(queue="second_testing")
    #     )

    res_one = chord(first_queue_tasks)(
        summarize.s().set(queue="first_testing")
    )

    # res_two = chord(second_queue_tasks)(
    #     summarize.s().set(queue="second_testing")
    # )

    elapsed_time = get_utc_timestamp() - start
    logger.info(
        f"Finished producing chords for both queues in {elapsed_time: .2f} "
        f"seconds."
    )
    logger.info(f"Chord One: {res_one}")
    # logger.info(f"Chord Two: {res_two}")


if __name__ == "__main__":
    produce()
