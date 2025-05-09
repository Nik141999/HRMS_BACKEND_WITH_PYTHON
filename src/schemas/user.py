from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email : EmailStr
    username : str

class UserCreate(UserBase):
    password : str
   
class UserLogin(UserBase):
    email : EmailStr  
    password : str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : Optional[str] = None
