from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.org_dao import *
from src.schemas.org_schema import OrgCreate, OrgUpdate, OrgResponse
from src.utils.auth import get_hash_password

async def create_org_service(org: OrgCreate, db: AsyncSession) -> OrgResponse:
    if await get_org_by_email(db, org.email):
        raise ValueError("Email already registered")

    role = await get_role_by_name(db, org.role_type)
    if not role:
        raise ValueError("Invalid role_type")

    hashed_password = get_hash_password(org.password)
   
    new_org = await create_org_in_db(
        db=db,
        org_name=org.org_name,
        email=org.email,
        hashed_password=hashed_password,
        role_id=role.id,
        address=org.address,
        phone_number=org.phone_number,
        industry=org.industry,
        description=org.description,
        website=org.website,
        gst_number=org.gst_number,
    )

    return OrgResponse.model_validate(new_org)

async def get_all_org_service(db: AsyncSession):
    orgs = await get_all_org(db)
    return [OrgResponse.model_validate(org) for org in orgs]

async def update_org_service(org_id: str, org_data: OrgUpdate, db: AsyncSession) -> OrgResponse:
    update_dict = org_data.dict(exclude_unset=True)
    if "password" in update_dict:
        update_dict["password"] = get_hash_password(update_dict["password"])
    
    org = await update_org_in_db(db, org_id, update_dict)
    if not org:
        raise ValueError("Organization not found")
    return OrgResponse.model_validate(org)

async def delete_org_service(org_id: str, db: AsyncSession):
    org = await delete_org_from_db(db, org_id)
    if not org:
        raise ValueError("Organization not found")
    return {"detail": "Organization deleted successfully"}
