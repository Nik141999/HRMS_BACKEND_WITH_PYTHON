from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth import get_current_user
from src.utils.permission_checker import PermissionChecker
from src.controller.user_controller import (
    create_user_controller,
    get_user_controller,
    update_user_controller,
    delete_user_controller,
    get_all_users_controller
)
from src.schemas.user import UserCreate, UserResponse
from src.database import get_db

router = APIRouter(tags=["User"], dependencies=[Depends(get_current_user)])

@router.post("/create_user", response_model=UserResponse, dependencies=[Depends(PermissionChecker("/create_user", "create"))])
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user_controller(user, db)

@router.get("/user/{user_id}", response_model=UserResponse, dependencies=[Depends(PermissionChecker("/user/{user_id}", "view"))])
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await get_user_controller(user_id, db)

@router.get("/users", response_model=list[UserResponse], dependencies=[Depends(PermissionChecker("/users", "view"))])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users_controller(db)

@router.put("/user/{user_id}", response_model=UserResponse, dependencies=[Depends(PermissionChecker("/user/{user_id}", "edit"))])
async def update_user(user_id: str, email: str, db: AsyncSession = Depends(get_db)):
    return await update_user_controller(user_id, email, db)

@router.delete("/user/{user_id}", dependencies=[Depends(PermissionChecker("/user/{user_id}", "delete"))])
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await delete_user_controller(user_id, db)
