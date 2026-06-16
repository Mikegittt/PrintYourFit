from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str
    target_campus: Optional[str] = None
    referral_code: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
