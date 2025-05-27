from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    role_id: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role_type: str
    user: UserResponse
    
class Token(BaseModel):
    access_token: str
    token_type: str
    role_type: str 
    

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
