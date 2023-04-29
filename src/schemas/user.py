from pydantic import BaseModel


class NewUser(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    access_token: str
    token_type: str


class UserInDB(BaseModel):
    id: int
    name: str
    hashed_password: str

    class Config:
        orm_mode = True
