from fastapi import Depends, HTTPException, status
from backend.auth import get_current_user


def require_role(allowed_roles):

    def role_checker(user=Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
        return user

    return role_checker
