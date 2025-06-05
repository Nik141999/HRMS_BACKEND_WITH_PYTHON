from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.organization import Organization
from src.models.role import Role
from src.models.user import User

async def get_role_by_name(db: AsyncSession, role_type: str):
    result = await db.execute(select(Role).where(Role.role_type == role_type.lower()))
    return result.scalars().first()


async def get_org_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalars().first()


async def get_org_by_id(db: AsyncSession, org_id: str):
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    return result.scalars().first()

async def get_all_org(db: AsyncSession):
    result = await db.execute(select(Organization))
    return result.scalars().all()

# src/dao/org_dao.py
async def create_org_in_db(
    db: AsyncSession,
    org_name: str,
    email: str,
    hashed_password: str,
    role_id: str,
    address: str = None,
    phone_number: str = None,
    industry: str = None,
    description: str = None,
    website: str = None,
    gst_number: str = None,
):
    new_org = Organization(
        org_name=org_name,
        address=address,
        phone_number=phone_number,
        industry=industry,
        description=description,
        website=website,
        gst_number=gst_number
    )
    db.add(new_org)
    await db.flush()  # Get new_org.id

    new_user = User(
        email=email,
        password=hashed_password,
        role_id=role_id,
        organization_id=new_org.id
    )
    db.add(new_user)

    await db.commit()
    await db.refresh(new_org)
    return new_org


async def update_org_in_db(db: AsyncSession, org_id: str, update_data: dict):
    org = await get_org_by_id(db, org_id)
    if org:
        for key, value in update_data.items():
            setattr(org, key, value)
        await db.commit()
        await db.refresh(org)
    return org

async def delete_org_from_db(db: AsyncSession, org_id: str):
    org = await get_org_by_id(db, org_id)
    if org:
        await db.delete(org)
        await db.commit()
    return org
