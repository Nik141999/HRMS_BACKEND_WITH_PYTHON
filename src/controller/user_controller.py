from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.service.user_service import create_user_service
from src.schemas.user import UserCreate

async def create_user_controller(user: UserCreate, db: AsyncSession):
    try:
        return await create_user_service(user, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
