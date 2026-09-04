from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=12)

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name:  Optional[str] = None
        

class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password : str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
