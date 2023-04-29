from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core import app_settings
from src.core.logging_config import logger
from src.db import get_session
from src.schemas.user import NewUser, UserInDB, UserToken
from src.services.user import user_crud, create_access_token
from src.utils.pwd import verify_password

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post(
    "/signup",
    response_model=UserInDB,
    description="Creates a new user account"
)
async def signup(
        *, schema: NewUser, session: AsyncSession = Depends(get_session)
) -> Response:
    try:
        res = await user_crud.add(session=session, schema=schema)
        logger.info("User '%s' is added", schema.name)
        return res
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Username '{schema.name}' is taken. Try another one.",
        )


@user_router.post(
    "/signin",
    response_model=UserToken,
    description="Endpoint for user authentication"
)
async def signin(
        *,
        session: AsyncSession = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    logger.info("Signing in as '%s'", form_data.username)
    user = await user_crud.get(session=session, username=form_data.username)
    if not user:
        logger.exception("No '%s' in the DB", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User was not found",
        )
    if verify_password(form_data.password, user.hashed_password):
        access_token_expires = timedelta(
            minutes=app_settings.jwt_expiration_time
        )
        access_token = create_access_token(
            data={"sub": user.name}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    logger.exception("Attempt to sign in with an invalid password")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password",
    )
