from sqlalchemy import Column, String, Boolean,DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

from src.utils.utils import generate_uuid

class UserBase(DeclarativeBase):
    pass

class User(UserBase):
    __tablename__ = 'users'

    id = Column(VARCHAR(512),primary_key=True,default=generate_uuid)
    email = Column(String(90), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255), nullable=False) 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
