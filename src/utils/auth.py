from typing import Optional, Dict
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from src.models.user import User
from src import config
from src.database import get_db

# Custom auth header
oauth2_scheme = APIKeyHeader(name="Authorization")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"

# ----------------------------- Password Hashing -----------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_hash_password(password: str) -> str:
    return pwd_context.hash(secret=password)

# ----------------------------- Authentication ------------------------------

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(User).options(selectinload(User.role)).where(User.email == email)
    )
    user = result.scalars().first()

    if not user or not verify_password(password, user.password):
        return False

    return user

# ----------------------------- Token Creation ------------------------------

def create_access_token(
    data: Dict[str, str],
    expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ----------------------------- Current User Dependency ------------------------------

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]

        # Decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        org_id: Optional[str] = payload.get("org_id")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Fetch user from database
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    # Attach org_id from token to user object (even if None)
    user.token_org_id = org_id
    return user
