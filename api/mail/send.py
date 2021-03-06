import os

from pydantic import BaseModel, EmailStr, AnyHttpUrl
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# from fastapi_mail.email_utils import DefaultChecker

import config

config.parse_args()


class Body(BaseModel):
    username: str
    confirm_url: AnyHttpUrl


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME") or config.CONFIG.mail_username,
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD") or config.CONFIG.mail_password,
    MAIL_FROM=os.getenv("MAIL_USERNAME")
    or config.CONFIG.mail_username
    or "user@example.com",
    MAIL_PORT=int(config.CONFIG.mail_port),
    MAIL_SERVER=config.CONFIG.mail_server,
    MAIL_FROM_NAME=config.CONFIG.mail_from,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="./api/mail",
)


async def user(to: EmailStr, body: Body):
    message = MessageSchema(
        subject="Confirm your email address", recipients=[to], body=body, subtype="html"
    )
    if (os.getenv("MAIL_USERNAME") and os.getenv("MAIL_PASSWORD")) or (
        config.CONFIG.mail_username and config.CONFIG.mail_password
    ):
        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")