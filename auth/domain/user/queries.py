import sqlalchemy as sa
from models.user import User


def email_exists(email: str) -> sa.Select:
    return sa.select(sa.exists().where(User.email == email))


def get_user_by_login_query(login: str) -> sa.Select:
    return sa.select(User.id).where(User.login == login)
