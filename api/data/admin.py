from constants import (
    USERS_TABLE,
    APPS_TABLE,
    RATINGS_TABLE,
    DOCS_TABLE,
    USERNAME_KEY,
    ROLE_KEY,
    EMAIL_KEY,
)

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
def admin_set_username_role(db, username, role):
    table = db[USERS_TABLE]
    table.update(
        {USERNAME_KEY: username, ROLE_KEY: role},
        [USERNAME_KEY],
    )


@connect_db
def admin_set_email_role(db, email, role):
    table = db[USERS_TABLE]
    table.update(
        {EMAIL_KEY: email, ROLE_KEY: role},
        [EMAIL_KEY],
    )


@connect_db
def admin_remove_user(db, user_id):
    table_users = db[USERS_TABLE]
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    # table_docs = db[DOCS_TABLE]
    table_apps.delete(owner=user_id)
    table_ratings.delete(user=user_id)
    table_users.delete(id=user_id)
    # table_docs.delete(application=app_id)


@connect_db
def admin_remove_application(db, app_id):
    table_apps = db[APPS_TABLE]
    table_ratings = db[RATINGS_TABLE]
    table_docs = db[DOCS_TABLE]
    table_ratings.delete(application=app_id)
    table_apps.delete(id=app_id)
    table_docs.delete(application=app_id)


@connect_db
def admin_remove_rating(db, rating_id):
    table = db[RATINGS_TABLE]
    table.delete(id=rating_id)


@connect_db
def admin_remove_documentation(db, doc_id):
    table = db[DOCS_TABLE]
    table.delete(id=doc_id)