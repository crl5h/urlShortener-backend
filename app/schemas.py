from fastapi_users import schemas
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLRequest(BaseModel):
    long_url: HttpUrl


class URLResponse(BaseModel):
    url: HttpUrl


class ClickLogResponse(BaseModel):
    short_id: str
    clicked_at: datetime


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
