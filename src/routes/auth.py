from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserResponse, UserCreate, Token
from src.database import get_db
from src.service.user_service import create_user_service
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from src.utils.auth import authenticate_user, create_access_token, get_current_user
from src.models.user import User


router = APIRouter(
    tags=["authentication"]
)


@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Reuse create_user_service which handles role validation & creation
        created_user = await create_user_service(user, db)
        return created_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.email, "role_type": user.role_id},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role_type=user.role_id
    )

@router.get("/me")
async def read_logged_in_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role_id
    }
