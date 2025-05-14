from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.user_dao import (
    get_user_by_email,
    get_user_by_id,
    create_user_in_db,
    update_user_in_db,
    delete_user_from_db,
    get_all_users
)
from src.schemas.user import UserCreate, UserResponse
from src.utils.auth import get_hash_password

async def create_user_service(user: UserCreate, db: AsyncSession) -> UserResponse:
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already registered")
    hashed_password = get_hash_password(user.password)
    new_user = await create_user_in_db(db, user.email, hashed_password)
    return UserResponse(id=new_user.id, email=new_user.email)

async def get_user_service(user_id: str, db: AsyncSession) -> UserResponse:
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    return UserResponse(id=user.id, email=user.email)

async def get_all_users_service(db: AsyncSession):
    users = await get_all_users(db)
    return [UserResponse(id=user.id, email=user.email) for user in users]
    

async def update_user_service(user_id: str, new_email: str, db: AsyncSession) -> UserResponse:
    user = await update_user_in_db(db, user_id, new_email)
    if not user:
        raise ValueError("User not found")
    return UserResponse(id=user.id, email=user.email)

async def delete_user_service(user_id: str, db: AsyncSession):
    user = await delete_user_from_db(db, user_id)
    if not user:
        raise ValueError("User not found")
    return {"detail": "User deleted successfully"}
