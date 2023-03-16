from pony.orm import Database


def get_database(filepath):
    return Database("sqlite", filepath, create_db=True)
