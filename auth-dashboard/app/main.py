from __future__ import annotations

from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"

def add_frontend(app):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

import hashlib
import hmac
import json
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

SECRET = b"dev-secret"
bearer = HTTPBearer(auto_error=False)

class UserIn(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=64)

def _b64(data: bytes) -> str:
    return urlsafe_b64encode(data).rstrip(b"=").decode()

def _unb64(text: str) -> bytes:
    padding = "=" * (-len(text) % 4)
    return urlsafe_b64decode(text + padding)

def make_token(username: str) -> str:
    payload = _b64(json.dumps({"sub": username, "exp": int(time.time()) + 3600}).encode())
    header = _b64(b'{"alg":"HS256"}')
    signing = f"{header}.{payload}".encode()
    sig = _b64(hmac.new(SECRET, signing, hashlib.sha256).digest())
    return f"{header}.{payload}.{sig}"

def read_token(token: str) -> str:
    try:
        header, payload, sig = token.split(".")
        signing = f"{header}.{payload}".encode()
        expected = _b64(hmac.new(SECRET, signing, hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected):
            raise ValueError("bad sig")
        data = json.loads(_unb64(payload))
        if data["exp"] < time.time():
            raise ValueError("expired")
        return data["sub"]
    except Exception as exc:
        raise HTTPException(401, "Invalid token") from exc

def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 50_000).hex()

def create_app() -> FastAPI:
    app = FastAPI(title="JWT Auth API", version="1.0.0")
    app.state.users: dict[str, str] = {}

    def current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> str:
        if creds is None:
            raise HTTPException(401, "Not authenticated")
        return read_token(creds.credentials)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/register", status_code=201)
    def register(payload: UserIn):
        if payload.username in app.state.users:
            raise HTTPException(409, "Username taken")
        app.state.users[payload.username] = hash_password(payload.password)
        return {"username": payload.username}

    @app.post("/login")
    def login(payload: UserIn):
        stored = app.state.users.get(payload.username)
        if stored is None or stored != hash_password(payload.password):
            raise HTTPException(401, "Invalid credentials")
        return {"access_token": make_token(payload.username), "token_type": "bearer"}

    @app.get("/me")
    def me(username: str = Depends(current_user)):
        return {"username": username}

    add_frontend(app)
    return app

app = create_app()
