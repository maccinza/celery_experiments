from os import getcwd

from pony.orm import PrimaryKey, Required, db_session

from utils.db import get_database

db = get_database(f"{getcwd()}/webserver.sqlite")


class SortingRecord(db.Entity):
    id = PrimaryKey(str)
    array = Required(bytes)
    time_is_sec = Required(str)


db.generate_mapping(create_tables=True)


@db_session
def insert_and_assert(attributes: dict) -> bool:
    SortingRecord(**attributes)
    return SortingRecord.exists(id=attributes["id"])
