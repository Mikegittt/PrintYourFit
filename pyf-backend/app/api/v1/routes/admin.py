from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.v1.deps import get_db, require_role
from app.models.user import User

router = APIRouter()

@router.get("/users", dependencies=[Depends(require_role("ADMIN"))])
async def list_users(db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Service unavailable")
    result = await db.execute(select(User))
    users = result.scalars().all()
    items = []
    for u in users:
        items.append({
            "id": str(u.id),
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "kyc_completed": u.kyc_completed,
            "created_at": str(u.created_at),
        })
    return items
