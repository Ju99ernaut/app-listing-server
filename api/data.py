import dataset

import config
from constants import *

from utils.db import connect_db

"""Functions for managing a dataset SQL database
    # Schemas

    #################### applications ######################
    image: str
    title: str
    by: str
    groups: [str]
    owner: user
    
    #################### ratings ##########################
    user: user
    application: application
    rating: float

    #################### users ############################
    username: str
    email: str
    password: str
    disablled: bool

"""


@connect_db
def add_application(db, image, title, by, groups, owner):
    table = db[APPS_TABLE]
    table.upsert(
        {
            IMAGE_KEY: image,
            TITLE_KEY: title,
            BY_KEY: by,
            GROUPS_KEY: groups,
            OWNER_KEY: owner,
        },
        [TITLE_KEY, OWNER_KEY],
    )


@connect_db
def remove_application(db, title):
    table = db[APPS_TABLE]
    table.delete(title=title)


@connect_db
def get_application(db, title):
    table = db[APPS_TABLE]
    row = table.find_one(title=title)
    if row is not None:
        return row
    return None


@connect_db
def get_all_applications(db):
    table = db[APPS_TABLE]
    all_items = table.all()
    return all_items


@connect_db
def add_rating(db, user, application, rating):
    table = db[RATINGS_TABLE]
    table.upsert(
        {
            USER_KEY: user,
            APPLICATION_KEY: application,
            RATING_KEY: rating,
        },
        [USER_KEY, APPLICATION_KEY, RATING_KEY],
    )


@connect_db
def get_user_rating(db, user):
    table = db[RATINGS_TABLE]
    row = table.find_one(user=user)
    if row is not None:
        return row
    return None


@connect_db
def get_application_rating(db, application):
    table = db[RATINGS_TABLE]
    row = table.find(application=application)
    avg_rating = sum([rating[RATING_KEY] for rating in row]) / row.count()
    if row is not None:
        return avg_rating
    return None


@connect_db
def get_all_ratings(db):
    table = db[RATINGS_TABLE]
    apps = [app[APPLICATION_KEY] for app in table.distinct(APPLICATION_KEY)]
    all_items = []
    for app in apps:
        all_items.append(
            {
                APPLICATION_KEY: app,
                RATING_KEY: get_application_rating(app),
            }
        )
    return all_items


@connect_db
def add_user(db, username, email, password, disabled):
    table = db[USERS_TABLE]
    table.upsert(
        {
            USERNAME_KEY: username,
            EMAIL_KEY: email,
            PASSWORD_KEY: password,
            DISABLED_KEY: disabled,
        },
        [USERNAME_KEY, EMAIL_KEY],
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