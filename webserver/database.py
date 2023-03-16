from pony.orm import Database, PrimaryKey, Required, db_session, select

db = Database("sqlite", "wbserver.sqlite", create_db=True)


class FibonacciRecord(db.Entity):
    id = PrimaryKey(str)
    number = Required(int)
    fibonacci = Required(str)
    timestamp = Required(str)


db.generate_mapping(create_tables=True)


@db_session
def insert_and_assert(attributes: dict) -> bool:
    # import ipdb; ipdb.set_trace()
    FibonacciRecord(**attributes)
    return FibonacciRecord.exists(id=attributes["id"])
