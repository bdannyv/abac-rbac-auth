import sqlalchemy as sa
from models.user import User


def email_exists(email: str):
    return sa.select(sa.exists().where(User.email == email)).with_for_update()
