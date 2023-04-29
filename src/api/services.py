import time

from aiobotocore.client import AioBaseClient
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.utils.s3 import get_s3_client

service_router = APIRouter(prefix="/services", tags=["Service"])


@service_router.get(
    "/ping",
    description="Health check of external services' connectivity"
)
async def get_ping(
        session: AsyncSession = Depends(get_session),
        s3_client: AioBaseClient = Depends(get_s3_client),
) -> dict:
    db_start = time.monotonic()
    await session.scalar(select(1))
    db_ping = time.monotonic() - db_start

    s3_start = time.monotonic()
    await s3_client.list_buckets()
    s3_ping = time.monotonic() - s3_start

    return {
        "DB": "{:.3f}".format(db_ping),
        "S3": "{:.3f}".format(s3_ping),
    }
