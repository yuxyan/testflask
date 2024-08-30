from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    privilege: str = 'Public'


class UserCreate(UserBase):
    password: str
