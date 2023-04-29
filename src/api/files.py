from io import BytesIO

from aiobotocore.client import AioBaseClient
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.openapi.models import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import StreamingResponse

from src.core import app_settings
from src.db import get_session
from src.models import UserModel
from src.schemas.file import FileInDB, UserFile
from src.services.file import file_crud
from src.services.user import get_current_user
from src.utils.s3 import get_s3_client

file_router = APIRouter(prefix="/files", tags=["File"])


@file_router.post(
    "/upload",
    response_model=FileInDB,
    status_code=status.HTTP_201_CREATED,
    description="Allows a user to upload a file to the server",
)
async def upload_file(
        *,
        file: UploadFile = File(),
        session: AsyncSession = Depends(get_session),
        user: UserModel = Depends(get_current_user),
        s3_client: AioBaseClient = Depends(get_s3_client),
) -> Response:
    await s3_client.put_object(
        Bucket=app_settings.s3_bucket,
        Key=f"{user.id}_{user.name}/{file.filename}",
        Body=file.file,
    )
    return await file_crud.create(session=session, file=file, user=user)


@file_router.get(
    "/download",
    status_code=status.HTTP_200_OK,
    description="Retrieves a file from the S3 bucket and streams back to the user",
)
async def download_file(
        *,
        file_id: int,
        session: AsyncSession = Depends(get_session),
        user: UserModel = Depends(get_current_user),
        s3_client: AioBaseClient = Depends(get_s3_client),
) -> StreamingResponse:
    file = await file_crud.get(
        session=session, file_id=file_id, user_id=user.id
    )
    response = await s3_client.get_object(
        Bucket=app_settings.s3_bucket,
        Key=f"{user.id}_{user.name}/{file.name}",
    )
    file_content = await response["Body"].read()
    return StreamingResponse(
        BytesIO(file_content), media_type=response["ContentType"]
    )


@file_router.get(
    "",
    response_model=UserFile,
    status_code=status.HTTP_200_OK,
    description="Retrieves a list of all files uploaded by the user to the server",
)
async def get_user_files(
        *,
        session: AsyncSession = Depends(get_session),
        user: UserModel = Depends(get_current_user),
) -> UserFile:
    files = await file_crud.get_batch(session=session, user_id=user.id)
    return UserFile(user_id=user.id, files=files)
