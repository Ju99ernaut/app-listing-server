import os
from datetime import datetime

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
    
    #################### documentations ######################
    application: application
    status: str
    external: str
    documentation: str
    updated: datetime
    
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
    active: bool
    role: str

"""


@connect_db
def admin(db):
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
                ACTIVE_KEY: True,
                ROLE_KEY: "admin",
            },
            [USERNAME_KEY, EMAIL_KEY],
        )


@connect_db
def migrate(db):
    users_table = db[USERS_TABLE]
    apps_table = db[APPS_TABLE]

    users_table.create_column(USERNAME_KEY, db.types.text, unique=True, nullable=False)
    users_table.create_column(EMAIL_KEY, db.types.text, unique=True, nullable=False)

    apps_table.create_column(TITLE_KEY, db.types.text, unique=True, nullable=False)