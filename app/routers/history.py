from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ClickLogResponse
from crud import get_click_logs
from db import get_async_session, User
from typing import List
from users import current_active_user
router = APIRouter()


@router.get("/{short_id}/analytics", response_model=List[ClickLogResponse])
async def get_analytics(short_id: str, db: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    click_logs = await get_click_logs(db, short_id)  # Await the async function
    if not click_logs:
        raise HTTPException(status_code=404, detail="No analytics found for this URL")
    return [
        ClickLogResponse(short_id=log.short_id, clicked_at=str(log.clicked_at))
        for log in click_logs
    ]
