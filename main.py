from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import hashlib

app = FastAPI()

characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

url_mapping = {}

class URLRequest(BaseModel):
    long_url: HttpUrl


@app.get("/")
def read_root():
    return {"hi": "works"}


@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_id = generate_unique_id(request.long_url)

    # Check for collision
    if short_id in url_mapping:
        raise HTTPException(status_code=400, detail="Short URL already exists.")
    
    url_mapping[short_id] = request.long_url

    short_url = f"http://localhost:8000/{short_id}"
    return {"short_url": short_url}


@app.get("/{short_id}")
def redirect_url(short_id: str):
    long_url = url_mapping.get(short_id)
    if long_url:
        return RedirectResponse(url=long_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")

def encode_base62(num):
    """ converts hashed value to base62 """
    if num == 0:
        return characters[0]
    base62 = []
    while num > 0:
        num, remainder = divmod(num, 62)
        base62.append(characters[remainder])
    return ''.join(reversed(base62))


def generate_unique_id(url):
    # get hashed url value
    while True:
        hash_object = hashlib.sha256(str(url).encode())
        hash_int = int(hash_object.hexdigest(), 16)
        short_id = encode_base62(hash_int)[:8]
        if short_id not in url_mapping:
            return short_id
