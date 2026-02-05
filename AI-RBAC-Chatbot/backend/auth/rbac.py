from fastapi import Depends, HTTPException, status
from backend.auth.dependencies import get_current_user

def require_roles(allowed_roles: list):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied : Documents not accessible by the selected role"
            )
        return current_user
    return role_checker
