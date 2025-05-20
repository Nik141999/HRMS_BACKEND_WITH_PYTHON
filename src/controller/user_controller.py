from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserCreate
from src.service.user_service import (
    create_user_service,
    get_user_service,
    update_user_service,
    delete_user_service,
    get_all_users_service
)

async def create_user_controller(user: UserCreate, db: AsyncSession):
    try:
        return await create_user_service(user, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def get_user_controller(user_id: str, db: AsyncSession):
    try:
        return await get_user_service(user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

async def get_all_users_controller(db: AsyncSession):
    return await get_all_users_service(db)

async def update_user_controller(user_id: str, email: str, db: AsyncSession):
    try:
        return await update_user_service(user_id, email, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

async def delete_user_controller(user_id: str, db: AsyncSession):
    try:
        return await delete_user_service(user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
