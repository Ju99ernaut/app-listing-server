import os


"""
 Constants useful for data module
"""
APPS_TABLE = "applications"
DOCS_TABLE = "documentations"
RATINGS_TABLE = "ratings"
USERS_TABLE = "users"

IMAGE_KEY = "image"
TITLE_KEY = "title"
BY_KEY = "by"
RATING_KEY = "rating"
GROUPS_KEY = "groups"
DESCRIPTION_KEY = "description"
DOCUMENTATION_KEY = "documentation"
UPDATED_KEY = "updated"
OWNER_KEY = "owner"

USER_KEY = "user"
APPLICATION_KEY = "application"
COMMENT_KEY = "comment"

USERNAME_KEY = "username"
EMAIL_KEY = "email"
PASSWORD_KEY = "password"
DISABLED_KEY = "disabled"
JOINED_KEY = "joined"
ACTIVE_KEY = "active"
ROLE_KEY = "role"

API_TAGS_METADATA = [
    {"name": "users", "description": "User data"},
    {"name": "applications", "description": "Application listing"},
    {"name": "ratings", "description": "Ratings and user feedback"},
    # {"name": "admin", "description": "Admin only"},
]

"""
 Constants useful for users module
"""
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = (
    os.getenv("SECRET_KEY")
    or "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
