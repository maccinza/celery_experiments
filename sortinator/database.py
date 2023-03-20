from enum import Enum
from os import getcwd
from pathlib import Path
import sys

from pony.orm import PrimaryKey, Required, StrArray, db_session

current = Path(__file__)
sys.path.insert(0, str(current.parent.parent.absolute()))

from utils.db import get_database

db = get_database(f"{getcwd()}/sortinator/sortinator.sqlite")


class TaskRunRecord(db.Entity):
    id = PrimaryKey(str)
    task_id = Required(str)
    success = Required(bool)
    start_timestamp = Required(float)
    end_timestamp = Required(float)
    data = Required(bytes)


class SummaryRecord(db.Entity):
    id = PrimaryKey(str)
    min_time =  Required(str)
    max_time = Required(str)
    avg_time = Required(str)
    min_length = Required(str)
    max_length = Required(str)
    avg_length = Required(str)
    task_ids = Required(StrArray)
    overall_success = Required(bool)


db.generate_mapping(create_tables=True)


class RecordTypeEnum(Enum):
    Task = TaskRunRecord
    Summary = SummaryRecord


@db_session
def insert_and_assert(record_type, attributes: dict) -> bool:
    record_type(**attributes)
    return record_type.exists(id=attributes["id"])
