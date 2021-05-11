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
def get_rating_by_id(db, rating_id):
    table_ratings = db[RATINGS_TABLE]
    table_users = db[USERS_TABLE]
    table_apps = db[APPS_TABLE]
    rating = table_ratings.find_one(id=rating_id)
    if rating is not None:
        rating[USER_KEY] = table_users.find_one(id=rating[USER_KEY])
        rating[APPLICATION_KEY] = table_apps.find_one(id=rating[APPLICATION_KEY])
        return rating
    return None


@connect_db
def get_user_application_ratings(db, user, application):
    table_ratings = db[RATINGS_TABLE]
    table_users = db[USERS_TABLE]
    table_apps = db[APPS_TABLE]
    rating = table_ratings.find_one(user=user, application=application)
    if rating is not None:
        rating[USER_KEY] = table_users.find_one(id=user)
        rating[APPLICATION_KEY] = table_apps.find_one(id=application)
        return rating
    return None


@connect_db
def get_user_ratings(db, user):
    table_ratings = db[RATINGS_TABLE]
    rows = table_ratings.find(user=user)
    if rows is not None:
        table_apps = db[APPS_TABLE]
        table_users = db[USERS_TABLE]
        user = table_users.find_one(id=user)

        return [
            {
                **ratings,
                USER_KEY: user,
                APPLICATION_KEY: table_apps.find_one(id=ratings[APPLICATION_KEY]),
            }
            for ratings in rows
        ]
    return None


@connect_db
def get_application_ratings(db, application):
    table_ratings = db[RATINGS_TABLE]
    rows = table_ratings.find(application=application)
    if rows is not None:
        table_users = db[USERS_TABLE]
        table_apps = db[APPS_TABLE]
        app = table_apps.find_one(id=application)

        return [
            {
                **ratings,
                USER_KEY: table_users.find_one(id=ratings[USER_KEY]),
                APPLICATION_KEY: app,
            }
            for ratings in rows
        ]
    return None


@connect_db
def get_all_ratings(db):
    table = db[RATINGS_TABLE]
    all_items = table.all()
    table_users = db[USERS_TABLE]
    table_apps = db[APPS_TABLE]
    return [
        {
            **ratings,
            USER_KEY: table_users.find_one(id=ratings[USER_KEY]),
            APPLICATION_KEY: table_apps.find_one(id=ratings[APPLICATION_KEY]),
        }
        for ratings in all_items
    ]


@connect_db
def remove_rating(db, rating_id, user):
    table = db[RATINGS_TABLE]
    table.delete(id=rating_id, user=user)


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
    apps = table.all()
    all_items = []
    for app in apps:
        all_items.append(
            {
                APPLICATION_KEY: app,
                RATING_KEY: get_average_rating(app["id"]),
            }
        )
    return all_items