from datetime import datetime

from constants import *

from utils.db import connect_db


@connect_db
def add_application(db, image, title, by, status, groups, description, owner):
    table = db[APPS_TABLE]
    table.insert(
        {
            IMAGE_KEY: image,
            TITLE_KEY: title,
            BY_KEY: by,
            STATUS_KEY: status,
            GROUPS_KEY: groups,
            DESCRIPTION_KEY: description,
            UPDATED_KEY: datetime.utcnow(),
            OWNER_KEY: owner,
        }
    )


@connect_db
def update_application(db, app_id, data):
    table = db[APPS_TABLE]
    table.update(
        {"id": app_id, **{k: v for k, v in data.dict().items() if v is not None}},
        ["id"],
    )


@connect_db
def remove_application(db, app_id, owner):
    table_apps = db[APPS_TABLE]
    table_docs = db[DOCS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    table_apps.delete(id=app_id, owner=owner)
    table_docs.delete(application=app_id)
    table_ratings.delete(application=app_id)


@connect_db
def get_application_by_id(db, app_id):
    table_apps = db[APPS_TABLE]
    table_users = db[USERS_TABLE]
    app = table_apps.find_one(id=app_id)
    if app is not None:
        app[OWNER_KEY] = table_users.find_one(id=app[OWNER_KEY])
        return app
    return None


@connect_db
def get_application(db, title):
    table_apps = db[APPS_TABLE]
    table_users = db[USERS_TABLE]
    app = table_apps.find_one(title=title)
    if app is not None:
        app[OWNER_KEY] = table_users.find_one(id=app[OWNER_KEY])
        return app
    return None


@connect_db
def get_user_applications(db, owner):
    table_apps = db[APPS_TABLE]
    rows = table_apps.find(owner=owner)
    if rows is not None:
        table_users = db[USERS_TABLE]
        user = table_users.find_one(id=owner)

        return [{**apps, OWNER_KEY: user} for apps in rows]
    return None


@connect_db
def get_all_applications(db):
    table_apps = db[APPS_TABLE]
    all_items = table_apps.all()
    table_users = db[USERS_TABLE]
    return [
        {**apps, OWNER_KEY: table_users.find_one(id=apps[OWNER_KEY])}
        for apps in all_items
    ]
