"""
 Constants useful for data module
"""
APPS_TABLE = "applications"
RATINGS_TABLE = "ratings"
RATING_TABLE = "rating"
USERS_TABLE = "users"

IMAGE_KEY = "image"
TITLE_KEY = "title"
BY_KEY = "by"
RATING_KEY = "rating"
GROUPS_KEY = "groups"
OWNER_KEY = "owner"

USER_KEY = "user"
APPLICATION_KEY = "application"

USERNAME_KEY = "username"
EMAIL_KEY = "email"
PASSWORD_KEY = "password"
DISABLED_KEY = "disabled"

API_TAGS_METADATA = [
    {"name": "items", "description": "Some random items"},
    {"name": "users", "description": "User data"},
]

"""
 Constants useful for users module
"""
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
