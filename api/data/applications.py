import os
from datetime import datetime

from constants import *

from utils.db import connect_db


@connect_db
def add_application(db, image, title, by, groups, description, owner):
    table = db[APPS_TABLE]
    table.insert(
        {
            IMAGE_KEY: image,
            TITLE_KEY: title,
            BY_KEY: by,
            GROUPS_KEY: groups,
            DESCRIPTION_KEY: description,
            UPDATED_KEY: datetime.utcnow(),
            OWNER_KEY: owner,
        }
    )


@connect_db
def update_application(db, id, data):
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    ##app = table_apps.find_one(id=id)
    ##if data[TITLE_KEY]:
    ##    rows = table_ratings.find(application=app[TITLE_KEY])
    ##    updated = ({**row, **dict(application=data[TITLE_KEY])} for row in rows)
    ##    table_ratings.upsert_many(updated, ["id"])
    table_apps.update(
        {"id": id, **{k: v for k, v in data.dict().items() if v is not None}}, ["id"]
    )


@connect_db
def remove_application(db, title, owner):
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    deleted = table_apps.delete(title=title, owner=owner)  #!
    table_ratings.delete(application=deleted["id"])


@connect_db
def get_application_by_id(db, id):
    table = db[APPS_TABLE]
    row = table.find_one(id=id)
    if row is not None:
        return row
    return None


@connect_db
def get_application(db, title):
    table = db[APPS_TABLE]
    row = table.find_one(title=title)
    if row is not None:
        return row
    return None


@connect_db
def get_user_applications(db, owner):
    table = db[APPS_TABLE]
    rows = table.find(owner=owner)
    if rows is not None:
        return rows
    return None


@connect_db
def get_all_applications(db):
    table = db[APPS_TABLE]
    all_items = table.all()
    return all_items