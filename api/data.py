import os
import dataset
from datetime import datetime

import config
from constants import *

from utils.db import connect_db
from utils.password import get_hash

"""Functions for managing a dataset SQL database
    # Schemas

    #################### applications ######################
    image: str
    title: str
    by: str
    groups: [str]
    description: str
    updated: datetime
    owner: user
    
    #################### ratings ##########################
    user: user
    application: application
    rating: float
    comment: str
    updated: datetime

    #################### users ############################
    username: str
    email: str
    password: str
    joined: datetime
    admin: bool

"""


@connect_db
def setup(db):
    # users = db[USERS_TABLE]
    # users.create_column(USERNAME_KEY, db.types.text, unique=True, nullable=False)
    # users.create_column(EMAIL_KEY, db.types.text, unique=True, nullable=False)

    # apps = db[APPS_TABLE]
    # apps.create_column(TITLE_KEY, db.types.text, unique=True, nullable=False)

    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    email = os.getenv("ADMIN_EMAIL")

    if username and password and email:
        table = db[USERS_TABLE]
        table.upsert(
            {
                USERNAME_KEY: username,
                EMAIL_KEY: email,
                PASSWORD_KEY: get_hash(password),
                JOINED_KEY: datetime.utcnow(),
                ADMIN_KEY: True,
            },
            [USERNAME_KEY, EMAIL_KEY],
        )


@connect_db
def add_application(db, image, title, by, groups, description, owner):
    table = db[APPS_TABLE]
    table.upsert(
        {
            IMAGE_KEY: image,
            TITLE_KEY: title,
            BY_KEY: by,
            GROUPS_KEY: groups,
            DESCRIPTION_KEY: description,
            UPDATED_KEY: datetime.utcnow(),
            OWNER_KEY: owner,
        },
        [TITLE_KEY, OWNER_KEY],
    )


@connect_db
def remove_application(db, title, owner):
    table = db[APPS_TABLE]
    table.delete(title=title, owner=owner)


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


@connect_db
def add_rating(db, user, application, rating, comment=None):
    table = db[RATINGS_TABLE]
    table.upsert(
        {
            USER_KEY: user,
            APPLICATION_KEY: application,
            RATING_KEY: rating,
            COMMENT_KEY: comment,
            UPDATED_KEY: datetime.utcnow(),
        },
        [USER_KEY, APPLICATION_KEY, RATING_KEY],
    )


@connect_db
def get_user_application_ratings(db, user, application):
    table = db[RATINGS_TABLE]
    row = table.find_one(user=user, application=application)
    if row is not None:
        return row
    return None


@connect_db
def get_user_ratings(db, user):
    table = db[RATINGS_TABLE]
    rows = table.find(user=user)
    if rows is not None:
        return rows
    return None


@connect_db
def get_application_ratings(db, application):
    table = db[RATINGS_TABLE]
    rows = table.find(application=application)
    if rows is not None:
        return rows
    return None


@connect_db
def get_all_ratings(db):
    table = db[RATINGS_TABLE]
    all_items = table.all()
    return all_items


@connect_db
def get_average_rating(db, application):
    table = db[RATINGS_TABLE]
    rows = table.find(application=application)
    avg_rating = sum([rating[RATING_KEY] for rating in rows]) / rows.count()
    if rows is not None:
        return avg_rating
    return None


@connect_db
def get_all_average_ratings(db):
    table = db[RATINGS_TABLE]
    apps = [app[APPLICATION_KEY] for app in table.distinct(APPLICATION_KEY)]
    all_items = []
    for app in apps:
        all_items.append(
            {
                APPLICATION_KEY: app,
                RATING_KEY: get_average_rating(app),
            }
        )
    return all_items


@connect_db
def add_user(db, username, email, password):
    table = db[USERS_TABLE]
    table.upsert(
        {
            USERNAME_KEY: username,
            EMAIL_KEY: email,
            PASSWORD_KEY: password,
            JOINED_KEY: datetime.utcnow(),
            ADMIN_KEY: False,
        },
        [USERNAME_KEY],
    )


@connect_db
def remove_user(db, username, email, password):
    table = db[USERS_TABLE]
    table.delete(username=username, email=email, password=password)


@connect_db
def get_user(db, username):
    table = db[USERS_TABLE]
    row = table.find_one(username=username)
    if row is not None:
        return row
    return None