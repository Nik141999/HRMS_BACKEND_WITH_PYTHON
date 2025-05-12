from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.controller.user_controller import create_user_controller
from src.schemas.user import UserCreate, UserResponse
from src.database import get_db

router = APIRouter()

@router.post("/create_user", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_user_controller(user, db)



