from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user_in_db(db: AsyncSession, email: str, hashed_password: str):
    new_user = User(email=email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
