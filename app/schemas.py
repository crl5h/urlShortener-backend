from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    long_url: HttpUrl

class URLResponse(BaseModel):
    short_url: str

class ClickLogResponse(BaseModel):
    short_id: str
    clicked_at: str

