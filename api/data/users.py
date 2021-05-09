import os
from datetime import datetime

from constants import *

from utils.db import connect_db


@connect_db
def add_user(db, username, email, password):
    table = db[USERS_TABLE]
    table.insert(
        {
            USERNAME_KEY: username,
            EMAIL_KEY: email,
            PASSWORD_KEY: password,
            JOINED_KEY: datetime.utcnow(),
            ACTIVE_KEY: False,
            ROLE_KEY: "user",
        },
    )


@connect_db
def update_user(db, id, data):
    table_users = db[USERS_TABLE]
    table_apps = db[APPS_TABLE]
    ##user = table_users.find_one(id=id)
    ##if data[USERNAME_KEY]:
    ##    rows = table_apps.find(owner=user[USERNAME_KEY])
    ##    updated = ({**row, **dict(owner=data[USERNAME_KEY])} for row in rows)
    ##    table_apps.upsert_many(updated, ["id"])
    table_users.update(
        {"id": id, **{k: v for k, v in data.dict().items() if v is not None}}, ["id"]
    )


@connect_db
def remove_user(db, username, email, password):
    table_users = db[USERS_TABLE]
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    deleted = table_users.delete(username=username, email=email, password=password)  #!
    table_apps.delete(owner=deleted["id"])
    table_ratings.delete(user=deleted["id"])


@connect_db
def get_user(db, username):
    table = db[USERS_TABLE]
    row = table.find_one(username=username)
    if row is not None:
        return row
    return None


@connect_db
def get_user_by_id(db, id):
    table = db[USERS_TABLE]
    row = table.find_one(id=id)
    if row is not None:
        return row
    return None


@connect_db
def get_user_by_email(db, email):
    table = db[USERS_TABLE]
    row = table.find_one(email=email)
    if row is not None:
        return row
    return None