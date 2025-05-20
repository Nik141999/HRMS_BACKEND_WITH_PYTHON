from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.roles_schema import RoleCreate, RoleUpdate, RoleOut
from src.controller.role_controller import RoleController
from src.utils.auth import get_current_user

router = APIRouter(tags=["Roles"], dependencies=[Depends(get_current_user)])
controller = RoleController()

@router.get("/get-roles", response_model=list[RoleOut])
async def get_roles(db: AsyncSession = Depends(get_db)):
    return await controller.get_roles(db)

@router.get("/get-roles/{role_id}", response_model=RoleOut)
async def get_role_by_id(role_id: int, db: AsyncSession = Depends(get_db)):
    return await controller.get_role_by_id(db, role_id)

@router.post("/create-role", response_model=RoleOut)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await controller.create_role(db, role)

@router.put("/update-role/{role_id}", response_model=RoleOut)
async def update_role(role_id: int, role: RoleUpdate, db: AsyncSession = Depends(get_db)):
    return await controller.update_role(db, role_id, role)
