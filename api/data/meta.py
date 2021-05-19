from constants import USERS_TABLE, APPS_TABLE, RATINGS_TABLE

from utils.db import connect_db


@connect_db
def get_users_count(db):
    return len(db[USERS_TABLE])


@connect_db
def get_apps_count(db):
    return len(db[APPS_TABLE])


@connect_db
def get_app_ratings_count(db, app_id):
    table = db[RATINGS_TABLE]
    return table.count(application=app_id)