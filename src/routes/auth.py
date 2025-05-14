from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from src.schemas.user import UserResponse, UserCreate, Token
from src.database import get_db
from src.models.user import User
from src.utils.auth import get_hash_password, authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user_by_email = result.scalars().first()
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_hash_password(user.password)

    db_user = User(
        email=user.email,
        password=hashed_password,
        role="user"  # Default role, change as needed
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        email=db_user.email,
    )


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    email = form_data.username

    user = await authenticate_user(
        db=db,
        email=email,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token_expires = timedelta(minutes=10)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},  # Include role in token
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role
    )
