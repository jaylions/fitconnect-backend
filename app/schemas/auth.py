from typing import Literal

from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: Literal["talent", "company"]


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    role: Literal["talent", "company"]
    token_type: str = "bearer"
