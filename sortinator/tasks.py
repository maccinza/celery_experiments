
from copy import deepcopy
from pickle import dumps

from celery import Celery
from celery.signals import after_setup_logger
from requests.status_codes import codes

from sortinator.celery_settings import base as CELERY_CONFIG
from sortinator.database import insert_and_assert, RecordTypeEnum
from utils.client import get_sorting
from utils.helpers import get_uuid, get_utc_timestamp
from utils.log import get_logger


logger = get_logger(__name__)
celery_app = Celery("sortinator.tasks", config_source=CELERY_CONFIG)


@celery_app.task(bind=True)
def sortinate(self):
    start_timestamp = get_utc_timestamp()

    logger.info(
        f"Started running sortinate task {self.request.id}, "
        f"will be getting a random sorting now."
    )

    status_code, response_data = get_sorting()
    success = False
    if status_code == codes.OK:
        success = True

    req_timestamp = get_utc_timestamp()
    elapsed_time = req_timestamp - start_timestamp

    logger.info(
        f"Finished requesting sorting in {elapsed_time: .2f} seconds."
    )

    data = {
        "id": get_uuid(),
        "task_id": self.request.id,
        "success": success,
        "start_timestamp": start_timestamp,
        "end_timestamp": req_timestamp,
        "data": response_data
    }

    db_data = deepcopy(data)
    db_data["data"] = dumps(db_data["data"])
    try:
        inserted = insert_and_assert(RecordTypeEnum.Task.value, db_data)
    except Exception as exc:
        inserted = False
        logger.error(f"Failed to insert and assert with exception. Got {exc}")
    finally:
        logger.info(
            f"Performed db insertion {'with' if inserted else 'without'} "
            f"success."
        )

    end_timestamp = get_utc_timestamp()
    elapsed_time = end_timestamp - start_timestamp

    logger.info(
        f"Finished running sortinate task {self.request.id} in "
        f"{elapsed_time: .2f} seconds."
    )

    return data


@celery_app.task(bind=True)
def summarize(self, tasks_data):
    start_timestamp = get_utc_timestamp()
    logger.info(f"Starting summarize task {self.request.id}.")

    summary = {
        "min_time": float("inf"),
        "max_time": 0,
        "avg_time": 0,
        "min_length": float("inf"),
        "max_length": 0,
        "avg_length": 0,
        "task_ids": [],
        "overall_success": False,
    }

    times = []
    lengths = []
    statuses = []
    for task_data in tasks_data:
        elapsed_time = (
            task_data["end_timestamp"] - task_data["start_timestamp"]
        )

        summary["min_time"] = min(summary["min_time"], elapsed_time)
        summary["max_time"] = max(summary["max_time"], elapsed_time)
        times.append(elapsed_time)

        statuses.append(task_data["success"])
        summary["task_ids"].append(task_data["task_id"])

        length = len(task_data["data"]["array"])
        summary["min_length"] = min(summary["min_length"], length)
        summary["max_length"] = max(summary["max_length"], length)
        lengths.append(length)

    summary["avg_time"] = sum(times)/len(times) if times else 0
    summary["avg_length"] = sum(lengths)/len(lengths) if lengths else 0
    summary["overall_success"] = all(statuses)

    db_summary = {"id": get_uuid(), **summary}
    db_summary["min_time"] = str(db_summary["min_time"])
    db_summary["max_time"] = str(db_summary["max_time"])
    db_summary["avg_time"] = str(db_summary["avg_time"])
    db_summary["min_length"] = str(db_summary["min_length"])
    db_summary["max_length"] = str(db_summary["max_length"])
    db_summary["avg_length"] = str(db_summary["avg_length"])

    try:
        inserted = insert_and_assert(RecordTypeEnum.Summary.value, db_summary)
    except Exception as exc:
        inserted = False
        logger.error(f"Failed to insert and assert with exception. Got {exc}")
    finally:
        logger.info(
            f"Performed db insertion {'with' if inserted else 'without'} "
            f"success."
        )

    logger.info(f"Summary: {summary}")

    elapsed_time = get_utc_timestamp() - start_timestamp
    logger.info(
        f"Finished summarize task {self.request.id} "
        f"in {elapsed_time: .2f} seconds."
    )

if __name__ == "__main__":
    celery_app.worker_main(
        [
            "-A",
            "sortinator.tasks",
            "worker",
            "--loglevel=info",
            "--without-gossip",
            "--without-mingle",
            "--heartbeat-interval=300",
        ]
    )
