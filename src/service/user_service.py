from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.user_dao import get_user_by_email, create_user_in_db
from src.schemas.user import UserCreate, UserResponse
from src.utils.auth import get_hash_password

async def create_user_service(user: UserCreate, db: AsyncSession) -> UserResponse:
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = get_hash_password(user.password)

    new_user = await create_user_in_db(db, user.email, hashed_password)

    return UserResponse(
        id=new_user.id,
        email=new_user.email
    )


