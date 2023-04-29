from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.schemas.user import NewUser

pytestmark = pytest.mark.asyncio


async def test_upload_file(test_user: NewUser, client: AsyncClient):
    filename = "test_file_1.txt"
    user_id = (
        await client.post("/user/signup", json=test_user.dict())
    ).json()["id"]
    form_data = {"username": test_user.name, "password": test_user.password}
    token = (await client.post("/user/signin", data=form_data)).json()[
        "access_token"
    ]

    response = await client.post(
        "files/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": (filename, b"Hello, World!")},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert "id" in response.json()
    assert response.json()["name"] == filename
    assert response.json()["size"] > 0
    assert response.json()["created_by"] == user_id


async def test_download_file(test_user: NewUser, client: AsyncClient):
    filename = "test_file_2.txt"
    await client.post("/user/signup", json=test_user.dict())
    form_data = {"username": test_user.name, "password": test_user.password}
    token = (
        await client.post("/user/signin", data=form_data)
    ).json()["access_token"]
    file_id = (
        await client.post(
            "files/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (filename, b"Hello, World!")},
        )
    ).json()["id"]

    response = await client.get(
        f"files/download?file_id={file_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.content == b"Hello, World!"
