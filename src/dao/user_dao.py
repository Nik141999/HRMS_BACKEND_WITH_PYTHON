from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.models.role import Role

async def get_role_by_name(db: AsyncSession, role_type: str):
    result = await db.execute(select(Role).where(Role.role_type == role_type.lower()))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user_in_db(db: AsyncSession, first_name: str, last_name: str, email: str, hashed_password: str, role_id: str):
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        role_id=role_id
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user_in_db(db: AsyncSession, user_id: str, new_email: str):
    user = await get_user_by_id(db, user_id)
    if user:
        user.email = new_email
        await db.commit()
        await db.refresh(user)
    return user

async def delete_user_from_db(db: AsyncSession, user_id: str):
    user = await get_user_by_id(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
    return user
