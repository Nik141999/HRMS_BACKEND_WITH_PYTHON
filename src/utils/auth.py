from typing import Optional,Dict
from datetime import datetime, timedelta,timezone

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt

from src.models.user import User
from src import config

 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_hash_password(password: str) -> str:
    return pwd_context.hash(secret=password)

async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(
    data: Dict[str, str],
    expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
