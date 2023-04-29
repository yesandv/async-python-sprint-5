from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Base
from src.utils.pwd import get_hashed_password

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class UserDBRepository(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: type(ModelType)):
        self._model = model

    async def add(
            self, *, session: AsyncSession, schema: CreateSchemaType
    ) -> ModelType:
        object_in_data = jsonable_encoder(schema)
        pwd = object_in_data.pop("password")
        object_in_data["hashed_password"] = get_hashed_password(pwd)
        db_object = self._model(**object_in_data)
        session.add(db_object)
        try:
            await session.commit()
            await session.refresh(db_object)
        except PendingRollbackError:
            await session.rollback()
            raise
        finally:
            await session.close()
        return db_object

    async def get(self, *, session: AsyncSession, username: str) -> ModelType:
        statement = select(self._model).where(self._model.name == username)
        results = await session.execute(statement=statement)
        return results.scalar_one_or_none()
