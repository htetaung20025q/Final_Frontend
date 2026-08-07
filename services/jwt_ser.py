from passlib.context import CryptContext
from datetime import datetime, timedelta
import bcrypt
from fastapi import HTTPException
import jwt
import secrets
from services.setting import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_minutes = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_refresh_token(expire_days: int = 7):
    token = secrets.token_urlsafe(48)
    expires_at = datetime.utcnow() + timedelta(days=expire_days)
    return token, expires_at
