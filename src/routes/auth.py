from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserResponse, UserCreate, Token
from src.database import get_db
from src.service.user_service import create_user_service
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from src.utils.auth import authenticate_user, create_access_token, get_current_user
from src.models.user import User
from src.schemas.user import LoginResponse, UserLogin


router = APIRouter(
    tags=["authentication"]
)


# @router.post("/register", response_model=UserResponse)
# async def register_user(
#     user: UserCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     try:
#         created_user = await create_user_service(user, db)
#         return created_user
#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )


@router.post("/login", response_model=LoginResponse)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token_expires = timedelta(minutes=960)
    access_token = create_access_token(
        data={"sub": user.email, "role_type": user.role.role_type},
        expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        role_type=user.role.role_type,
        user=UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role_id=user.role_id
        )
    )
    

@router.get("/me")
async def read_logged_in_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role_id
    }
