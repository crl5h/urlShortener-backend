import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import URL, ClickLog


async def create_url_mapping(db: AsyncSession, short_id: str, long_url: str, user_id: int):
    db_url_mapping = URL(short_id=short_id, long_url=long_url, user_id=user_id)
    db.add(db_url_mapping)
    await db.commit()
    await db.refresh(db_url_mapping)
    return db_url_mapping


async def get_long_url(db: AsyncSession, short_id: str):
    result = await db.execute(
        select(URL).filter(URL.short_id == short_id)
    )
    return result.scalars().first()  # Retrieve the first result from the async query


async def log_click(db: AsyncSession, short_id: str):
    click_log = ClickLog(short_id=short_id, clicked_at=datetime.datetime.now())
    db.add(click_log)
    await db.commit()
    await db.refresh(click_log)
    return click_log


async def get_click_logs(db: AsyncSession, short_id: str):
    result = await db.execute(select(ClickLog).filter(ClickLog.short_id == short_id))
    return result.scalars().all()
