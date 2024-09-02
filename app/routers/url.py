from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas import URLRequest, URLResponse
from crud import create_url_mapping, get_long_url, log_click
from utils import generate_unique_id
from db import User, get_async_session
from users import current_active_user
from config import settings

router = APIRouter()


@router.post(
    "/shorten",
    response_model=URLResponse,
)
async def shorten_url(
    request: URLRequest,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    short_id = generate_unique_id(request.long_url)

    existing_url = await get_long_url(db, short_id)
    if existing_url:
        raise HTTPException(status_code=400, detail="Short URL already exists.")

    await create_url_mapping(db, short_id, str(request.long_url), user.id)

    short_url = f"{settings.base_url}/{short_id}"

    return URLResponse(url=short_url)


@router.get(
    "/{short_id}",
    response_model=URLResponse,
)
async def resolve_url(
    short_id: str,
    db: AsyncSession = Depends(get_async_session)
):
    url_mapping = await get_long_url(db, short_id)
    if url_mapping:
        await log_click(db, short_id)
        return URLResponse(url=url_mapping.long_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
