from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from crud import get_click_logs
from schemas import ClickLogResponse
from db import get_db

router = APIRouter()

@router.get("/{short_id}/analytics", response_model=list[ClickLogResponse])
def get_analytics(short_id: str, db: Session = Depends(get_db)):
    click_logs = get_click_logs(db, short_id)
    if not click_logs:
        raise HTTPException(status_code=404, detail="No analytics found for this URL")
    return [ClickLogResponse(short_id=log.short_id, clicked_at=str(log.clicked_at)) for log in click_logs]
