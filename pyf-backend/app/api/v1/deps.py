from datetime import datetime
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.session import Session
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

SESSION_COOKIE_NAME = "sessionid"

async def get_current_user(
    session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    db: AsyncSession = Depends(get_db),
) -> User:
    logger.info(f"[AUTH] get_current_user called. session_id={session_id}")
    
    if not session_id:
        logger.warning("[AUTH] No session_id cookie provided")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    session = await db.get(Session, session_id)
    if not session:
        logger.warning(f"[AUTH] Session not found in DB: {session_id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")
    
    if session.expires_at and session.expires_at < datetime.utcnow():
        logger.warning(f"[AUTH] Session expired: {session.expires_at}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")

    user = await db.get(User, session.user_id)
    if not user:
        logger.error(f"[AUTH] User not found: {session.user_id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    logger.info(f"[AUTH] User authenticated: {user.email}")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def require_role(*roles: str):
    async def role_dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role privileges")
        return current_user
    return role_dependency
