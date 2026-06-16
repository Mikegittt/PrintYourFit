from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from app.api.v1.deps import get_db, require_role
from app.models.notification import Notification
from app.core.config import settings

router = APIRouter()

@router.post("/", dependencies=[Depends(require_role("ADMIN"))])
async def post_notification(payload: dict, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Service unavailable")
    title = payload.get("title")
    message = payload.get("message")
    if not title or not message:
        raise HTTPException(status_code=400, detail="title and message required")
    n = Notification(title=title, message=message, source=payload.get("source"))
    db.add(n)
    await db.commit()
    await db.refresh(n)

    # webhook dispatch
    webhook = getattr(settings, "NOTIFICATIONS_WEBHOOK_URL", None)
    if webhook:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(webhook, json={"id": str(n.id), "title": n.title, "message": n.message, "created_at": str(n.created_at)})
        except Exception:
            # Log and continue; do not fail the request
            pass

    return {"id": str(n.id), "title": n.title, "message": n.message, "created_at": str(n.created_at)}

@router.get("/", response_model=list[dict])
async def list_notifications(db: AsyncSession = Depends(get_db)):
    if db is None:
        return []
    result = await db.execute(select(Notification).where(Notification.active == True).order_by(Notification.created_at.desc()))
    items = result.scalars().all()
    return [{"id": str(i.id), "title": i.title, "message": i.message, "created_at": str(i.created_at)} for i in items]
