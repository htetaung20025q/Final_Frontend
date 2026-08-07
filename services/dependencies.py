from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import User
import services.jwt_ser as jwt_ser
from config.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token=Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt_ser.decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
        
    stmt = select(User).filter(User.id == payload["id"])
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found or Not authenticated"
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
