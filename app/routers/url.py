from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import URLRequest, URLResponse
from crud import create_url_mapping, get_long_url, log_click
from utils import generate_unique_id
from db import get_db

router = APIRouter()

@router.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    short_id = generate_unique_id(request.long_url)

    if get_long_url(db, short_id):
        raise HTTPException(status_code=400, detail="Short URL already exists.")
    
    create_url_mapping(db, short_id, str(request.long_url))

    short_url = f"http://localhost:8000/{short_id}"
    
    return URLResponse(short_url=short_url)

@router.get("/{short_id}", response_model=URLResponse)
def resolve_url(short_id: str, db: Session = Depends(get_db)):
    url_mapping = get_long_url(db, short_id)
    if url_mapping:
        log_click(db, short_id)
        return URLResponse(short_url=url_mapping.long_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
