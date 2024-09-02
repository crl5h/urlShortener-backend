from fastapi import FastAPI
from routers.url import router as url_router
from routers.history import router as history_router
from db import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"hi": "works"}

app.include_router(url_router, prefix="/api/urls")
app.include_router(history_router, prefix="/api/urls")
