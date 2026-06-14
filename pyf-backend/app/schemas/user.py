from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str
    target_campus: Optional[str] = None

class UserCreate(UserBase):
    password: str
    referral_code: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    target_campus: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: UUID
    referral_code: Optional[str] = None
    referred_by: Optional[UUID] = None
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
