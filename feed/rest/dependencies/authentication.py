from typing import Optional
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from feed.config import Settings, OAUTH_TOKEN_URL, OAUTH_SCHEME
from .config import get_config


auth_scheme = OAuth2PasswordBearer(
    tokenUrl=OAUTH_TOKEN_URL,
    scheme_name=OAUTH_SCHEME
)


def validate_access_token(token: str, key: str, algorithm: str) -> Optional[UUID]:
    """:returns: user id if token is correct, None if not"""
    try:
        data = jwt.decode(token, key, algorithms=[algorithm])
        user_id = data["sub"]
        return UUID(user_id)
    except Exception:
        return None


def authenticated_user_id(
        token: str = Depends(auth_scheme),
        config: Settings = Depends(get_config)) -> UUID:

    user_id = validate_access_token(token, config.JWT_KEY, config.JWT_ALGORITHM)

    if user_id is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Access token missing or not correct"
        )

    return user_id
