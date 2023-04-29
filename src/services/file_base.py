from typing import Generic, TypeVar

from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Base
from src.models import UserModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class FileDBRepository(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: type(ModelType)):
        self._model = model

    async def create(
            self, *, session: AsyncSession, file: UploadFile, user: UserModel
    ) -> ModelType:
        db_obj = self._model(
            name=file.filename, size=file.size, created_by=user.id
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(
            self, *, session: AsyncSession, file_id: int, user_id: int
    ) -> ModelType:
        statement = select(self._model).where(
            self._model.id == file_id and self._model.created_by == user_id
        )
        results = await session.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_batch(
            self, *, session: AsyncSession, user_id: int
    ) -> ModelType:
        statement = select(self._model).where(
            self._model.created_by == user_id
        )
        results = await session.execute(statement=statement)
        return results.scalars().all()
