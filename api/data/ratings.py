import os
from datetime import datetime

from constants import *

from utils.db import connect_db


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
        [USER_KEY, APPLICATION_KEY],
    )


@connect_db
def get_rating_by_id(db, id):
    table = db[RATINGS_TABLE]
    row = table.find_one(id=id)
    if row is not None:
        return row
    return None


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
def remove_rating(db, id, user):
    table = db[RATINGS_TABLE]
    table.delete(id=id, user=user)


@connect_db
def get_average_rating(db, application):
    table = db[RATINGS_TABLE]
    rows = table.find(application=application)
    ratings = [rating[RATING_KEY] for rating in rows]
    if not len(ratings):
        return 0
    avg_rating = sum(ratings) / len(ratings)
    if rows is not None:
        return avg_rating
    return 0


@connect_db
def get_all_average_ratings(db):
    table = db[APPS_TABLE]
    apps = [app[TITLE_KEY] for app in table.all()]
    all_items = []
    for app in apps:
        all_items.append(
            {
                APPLICATION_KEY: app,  #! Get Application
                RATING_KEY: get_average_rating(app),
            }
        )
    return all_items