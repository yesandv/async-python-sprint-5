from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import app_settings
from src.db import get_session
from src.models.user import UserModel
from src.schemas.user import NewUser, UserInDB
from src.services.user_base import UserDBRepository


class UserRepository(UserDBRepository[UserModel, NewUser, UserInDB]):
    pass


user_crud = UserRepository(UserModel)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        app_settings.jwt_secret_key,
        algorithm=app_settings.jwt_algorithm,
    )
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/signin")


async def get_current_user(
        session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme),
) -> UserModel:
    decoded_token = jwt.decode(
        token,
        app_settings.jwt_secret_key,
        algorithms=[app_settings.jwt_algorithm],
    )
    username = decoded_token.get("sub")
    return await user_crud.get(session=session, username=username)
