from datetime import datetime

from pydantic import BaseModel


class FileUpload(BaseModel):
    name: str
    created_by: int

    class Config:
        orm_mode = True


class FileInDB(BaseModel):
    id: int
    name: str
    size: int
    created_at: datetime
    created_by: int

    class Config:
        orm_mode = True


class UserFile(BaseModel):
    user_id: int
    files: list[FileInDB]

    class Config:
        orm_mode = True
