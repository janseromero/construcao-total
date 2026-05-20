"""Common FastAPI dependencies: current user, tenant scope, role gates."""

from collections.abc import Callable
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User, UserRole


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Invalid token: {exc}") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token payload")
    user = db.get(User, UUID(user_id))
    if not user or not user.ativo:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or inactive")
    return user


def require_role(*roles: UserRole) -> Callable[[User], User]:
    def _dep(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient role")
        return user

    return _dep


require_proprietario = require_role(UserRole.proprietario)
