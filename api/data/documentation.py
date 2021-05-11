from datetime import datetime

from constants import *

from utils.db import connect_db


@connect_db
def add_documentation(db, application, documentation):
    table = db[DOCS_TABLE]
    table.upsert(
        {
            APPLICATION_KEY: application,
            DOCUMENTATION_KEY: documentation,
            UPDATED_KEY: datetime.utcnow(),
        },
        [APPLICATION_KEY],
    )


@connect_db
def get_documentation_by_id(db, doc_id):
    table_docs = db[DOCS_TABLE]
    table_apps = db[APPS_TABLE]
    doc = table_docs.find_one(id=doc_id)
    if doc is not None:
        doc[APPLICATION_KEY] = table_apps.find_one(id=doc[APPLICATION_KEY])
        return doc
    return None


@connect_db
def get_documentation_by_app_id(db, app_id):
    table_docs = db[DOCS_TABLE]
    table_apps = db[APPS_TABLE]
    doc = table_docs.find_one(application=app_id)
    if doc is not None:
        doc[APPLICATION_KEY] = table_apps.find_one(id=app_id)
        return doc
    return None


@connect_db
def remove_documentation(db, doc_id):
    table = db[DOCS_TABLE]
    table.delete(id=doc_id)