from os import getcwd
from datetime import timezone

from pony.orm import PrimaryKey, Required, db_session

from utils.db import get_database

db = get_database(f"{getcwd()}/fibonator.sqlite")


class TaskRunRecord(db.Entity):
    id = PrimaryKey(str)
    task_id = Required(str)
    success = Required(bool)
    start_timestamp = Required(str)
    end_timestamp = Required(str)
    datastring = Required(str)


db.generate_mapping(create_tables=True)


@db_session
def insert_and_assert(attributes: dict) -> bool:
    TaskRunRecord(**attributes)
    return TaskRunRecord.exists(id=attributes["id"])
