from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import User
from schemas.user import UserCreate, UserUpdate, UserDelete, UserLogin
import services.jwt_ser as jwt_ser
from datetime import datetime, timedelta
from fastapi import HTTPException
from models.user_model import User as UserModel
from services.jwt_ser import create_access_token, verify_password
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from slowapi.util import get_remote_address
from slowapi import Limiter
import redis.asyncio as redis

REDIS_URL = "redis://localhost:6379/0"
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])


async def is_token_blacklisted(token: str) -> bool:
    return await redis_client.exists(f"bl_{token}") > 0


async def blacklist_token(token: str, expires_in: int):
    await redis_client.setex(f"bl_{token}", expires_in, "true")


async def login(user: UserLogin, session: AsyncSession):
    stmt = select(UserModel).where(UserModel.email == user.email)
    result = await session.execute(stmt)
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(data={"id": db_user.id})
    refresh_token = create_access_token(data={"id": db_user.id})

    response = JSONResponse(
        content={
            "Message": f"User {db_user.username} logged in successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "username": db_user.username,
                "is_admin": db_user.is_admin
            }
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        max_age=3600 * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        max_age=3600 * 24 * 7,
    )
    return response


async def register(user: UserCreate, db: AsyncSession):
    stmt = select(User).filter(User.email == user.email)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already exists")
        
    stmt_user = select(User).filter(User.username == user.username)
    result_user = await db.execute(stmt_user)
    if result_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username already exists")
        
    hashed_password = jwt_ser.hash_password(user.password)
    db_user = User(
        email=user.email, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    access_token = jwt_ser.create_access_token(data={"id": db_user.id})
    refresh_token = jwt_ser.create_access_token(data={"id": db_user.id})
    
    response = JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "username": db_user.username,
                "is_admin": db_user.is_admin
            },
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        max_age=3600 * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        max_age=3600 * 24 * 7,
    )
    return response


async def update(user: UserUpdate, db: AsyncSession):
    stmt = select(User).filter(User.id == user.id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    if not jwt_ser.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    if user.email is not None:
        db_user.email = user.email
    if user.username is not None:
        db_user.username = user.username
    if user.password:
        db_user.hashed_password = jwt_ser.hash_password(user.password)

    await db.commit()
    await db.refresh(db_user)
    return {
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username,
        }
    }


async def delete(user: UserDelete, db: AsyncSession):
    stmt = select(User).filter(User.id == user.id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    if not jwt_ser.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted successfully"}


async def refresh(refresh_token: str, db: AsyncSession):
    if await is_token_blacklisted(refresh_token):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    try:
        payload = jwt_ser.decode_token(refresh_token)
        user_id = payload.get("id")
    except Exception:
         raise HTTPException(status_code=401, detail="Invalid refresh token format")
         
    # rotate
    await blacklist_token(refresh_token, 3600 * 24 * 7)
    
    new_refresh, expires_at = jwt_ser.create_refresh_token()
    access_token = jwt_ser.create_access_token(data={"id": user_id})

    return {"access_token": access_token, "refresh_token": new_refresh}


async def logout(refresh_token: str, db: AsyncSession):
    await blacklist_token(refresh_token, 3600 * 24 * 7)
    return {"message": "Logged out successfully"}
