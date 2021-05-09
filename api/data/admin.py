import os

from constants import *

from utils.db import connect_db


@connect_db
def admin_get_user(db, id):
    table = db[USERS_TABLE]
    row = table.find_one(id=id)
    if row is not None:
        return row
    return None


@connect_db
def admin_get_users(db):
    table = db[USERS_TABLE]
    all_items = table.all()
    return all_items


@connect_db
def admin_remove_user(db, id):
    table_users = db[USERS_TABLE]
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    user = table_users.find_one(id=id)
    table_apps.delete(owner=user[USERNAME_KEY])
    table_ratings.delete(user=user[USERNAME_KEY])
    table_users.delete(id=id)


@connect_db
def admin_remove_application(db, id):
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    table_ratings.delete(application=id)
    table_apps.delete(id=id)


@connect_db
def admin_remove_rating(db, id):
    table = db[RATINGS_TABLE]
    table.delete(id=id)