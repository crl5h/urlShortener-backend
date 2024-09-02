from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db import Base
import datetime

class URLMapping(Base):
    __tablename__ = "url_mapping"

    short_id = Column(String, primary_key=True, index=True)
    long_url = Column(String, index=True)

class ClickLog(Base):
    __tablename__ = "click_log"

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, index=True)
    clicked_at = Column(DateTime, default=datetime.datetime.utcnow)
