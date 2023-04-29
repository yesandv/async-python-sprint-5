from typing import AsyncIterator

import aioboto3
from aiobotocore.client import AioBaseClient

from src.core import app_settings


async def get_s3_client() -> AsyncIterator[AioBaseClient]:
    s3_session = aioboto3.Session()
    async with s3_session.client(
        "s3",
        region_name=app_settings.s3_region,
        endpoint_url=app_settings.s3_endpoint,
        aws_access_key_id=app_settings.s3_key,
        aws_secret_access_key=app_settings.s3_secret_key,
    ) as client:
        yield client
