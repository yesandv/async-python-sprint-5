from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.schemas.user import NewUser
from src.utils.str_gen import get_username

pytestmark = pytest.mark.asyncio


async def test_signup(test_user: NewUser, client: AsyncClient):
    response = await client.post("/user/signup", json=test_user.dict())

    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == test_user.name
    assert response.json()["hashed_password"] != test_user.password


async def test_username_is_taken(client: AsyncClient):
    username = get_username()
    test_user_1 = NewUser(name=username, password="Qwerty12345")
    await client.post("/user/signup", json=test_user_1.dict())
    test_user_2 = NewUser(name=username, password="12345Qwerty")

    response = await client.post("/user/signup", json=test_user_2.dict())

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
            response.json()["detail"]
            == f"Username '{username}' is taken. Try another one."
    )


async def test_signin(test_user: NewUser, client: AsyncClient):
    await client.post("/user/signup", json=test_user.dict())
    form_data = {"username": test_user.name, "password": test_user.password}

    response = await client.post("/user/signin", data=form_data)

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


async def test_invalid_user(test_user: NewUser, client: AsyncClient):
    form_data = {"username": test_user.name, "password": test_user.password}

    response = await client.post("/user/signin", data=form_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "User was not found"


async def test_invalid_password(test_user: NewUser, client: AsyncClient):
    await client.post("/user/signup", json=test_user.dict())
    form_data = {"username": test_user.name, "password": "invalidPassword"}

    response = await client.post("/user/signin", data=form_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect password"
    assert "access_token" not in response.json()
    assert "token_type" not in response.json()
