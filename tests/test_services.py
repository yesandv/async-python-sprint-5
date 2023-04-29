from http import HTTPStatus

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_ping_status_code(client: AsyncClient):
    response = await client.get("services/ping")
    assert response.status_code == HTTPStatus.OK


async def test_ping_keys(client: AsyncClient):
    response = await client.get("services/ping")
    assert "DB" in response.json()
    assert "S3" in response.json()


async def test_ping_values(client: AsyncClient):
    response = await client.get("services/ping")
    assert float(response.json()["DB"]) > 0
    assert float(response.json()["S3"]) > 0
