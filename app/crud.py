from sqlalchemy.orm import Session
from models import URLMapping, ClickLog

def create_url_mapping(db: Session, short_id: str, long_url: str):
    db_url_mapping = URLMapping(short_id=short_id, long_url=long_url)
    db.add(db_url_mapping)
    db.commit()
    db.refresh(db_url_mapping)
    return db_url_mapping

def get_long_url(db: Session, short_id: str):
    return db.query(URLMapping).filter(URLMapping.short_id == short_id).first()

def log_click(db: Session, short_id: str):
    click_log = ClickLog(short_id=short_id)
    db.add(click_log)
    db.commit()
    db.refresh(click_log)
    return click_log

def get_click_logs(db: Session, short_id: str):
    return db.query(ClickLog).filter(ClickLog.short_id == short_id).all()
