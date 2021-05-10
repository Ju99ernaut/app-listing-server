import os

from constants import USERS_TABLE, APPS_TABLE, RATINGS_TABLE

from utils.db import connect_db


@connect_db
def admin_get_user(db, user_id):
    table = db[USERS_TABLE]
    row = table.find_one(id=user_id)
    if row is not None:
        return row
    return None


@connect_db
def admin_get_users(db):
    table = db[USERS_TABLE]
    all_items = table.all()
    return all_items


@connect_db
def admin_remove_user(db, user_id):
    table_users = db[USERS_TABLE]
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    table_apps.delete(owner=user_id)
    table_ratings.delete(user=user_id)
    table_users.delete(id=user_id)


@connect_db
def admin_remove_application(db, app_id):
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    table_ratings.delete(application=app_id)
    table_apps.delete(id=app_id)


@connect_db
def admin_remove_rating(db, rating_id):
    table = db[RATINGS_TABLE]
    table.delete(id=rating_id)