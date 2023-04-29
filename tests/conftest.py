import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from src.core import app_settings
from src.db import Base, get_session
from src.main import app
from src.schemas.user import NewUser
from src.utils.str_gen import get_username

TEST_DB = app_settings.base_dir + "/test.db"
TEST_DB_DSN = "sqlite+aiosqlite:///" + TEST_DB


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="session")
def _engine() -> AsyncEngine:
    return create_async_engine(url=TEST_DB_DSN, echo=True, future=True)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_session(_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as async_session:
        def get_override_dependency():
            return async_session

        app.dependency_overrides[get_session] = get_override_dependency
        yield async_session

    await _engine.dispose()


@pytest.fixture
def test_user() -> NewUser:
    return NewUser(name=get_username(), password="Qwerty12345")
