from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from auth.settings.auth import auth_settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a JWT access token.

    :param data: The data to encode in the token (e.g., {"sub": user_login}).
    :param expires_delta: Optional timedelta to override the default token expiry.
    :return: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=auth_settings.jwt_access_ttl)
    
    to_encode.update({"exp": expire})
    if auth_settings.jwt_iss:
        to_encode.update({"iss": auth_settings.jwt_iss})
    if auth_settings.jwt_aud:
        to_encode.update({"aud": list(auth_settings.jwt_aud)}) # Ensure it's a list if tuple

    encoded_jwt = jwt.encode(to_encode, auth_settings.jwt_key, algorithm=auth_settings.jwt_algo)
    return encoded_jwt
