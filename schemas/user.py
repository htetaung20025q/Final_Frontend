from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: bool = False


class UserCreate(UserBase):
    email: EmailStr
    username: str = Field(..., min_length=5, max_length=30)
    password: str = Field(..., min_length=5, max_length=30)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False
    is_active: bool = True


class UserUpdate(UserBase):
    id: int
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserDelete(BaseModel):
    id: int
    password: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
