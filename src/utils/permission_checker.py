from fastapi import Depends, HTTPException, status
from src.utils.auth import get_current_user
from src.models.user import User

def PermissionChecker(route: str, action: str):
    async def checker(user: User = Depends(get_current_user)):
        if not user.role or not user.role.permission:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role permissions not set.")

        permissions = user.role.permission 

        
        for perm in permissions:
            if perm.get("route") == route:
                allowed = perm.get("permission", {}).get(action)
                if not allowed:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"You do not have permission to perform this action"
                    )
                return  

       
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No permission rule defined for this route'"
        )
    return checker