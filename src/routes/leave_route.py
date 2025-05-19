from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import get_current_user
from src.schemas.leave_schema import LeaveCreate, LeaveResponse, LeaveUpdate
from src.utils.permission_checker import PermissionChecker
from src.controller.leave_controller import (
    create_leave_controller,
    get_all_leaves_controller,
    update_leave_controller,
    delete_leave_controller,
)
from src.database import get_db
from src.models.user import User

router = APIRouter(tags=["Leave"])

@router.post("/create_leave", response_model=LeaveResponse,dependencies=[Depends(PermissionChecker("/create_leave", "create"))])
async def create_leave(
    leave: LeaveCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_leave_controller(leave, db, current_user.id)

@router.get("/leaves", response_model=list[LeaveResponse],dependencies=[Depends(PermissionChecker("/leaves", "view"))])
async def get_all_leaves(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_all_leaves_controller(db, current_user.id)

@router.put("/update_leave/{leave_id}", response_model=LeaveResponse,dependencies=[Depends(PermissionChecker("/update_leave/{leave_id}", "edit"))])
async def update_leave(
    leave_id: str,
    leave: LeaveUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_leave_controller(leave_id, leave, db, current_user.id)

@router.delete("/delete_leave/{leave_id}",dependencies=[Depends(PermissionChecker("/delete_leave/{leave_id}", "delete"))])
async def delete_leave(
    leave_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_leave_controller(leave_id, db, current_user.id)
