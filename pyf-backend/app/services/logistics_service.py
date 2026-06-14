from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.logistics import Logistics
from app.models.order import Order

async def create_dispatch(db: AsyncSession, order_id, payload):
    logistics = Logistics(
        order_id=order_id,
        dispatcher_name=payload.dispatcher_name,
        tracking_notes=payload.tracking_notes,
        estimated_delivery=payload.estimated_delivery,
    )
    db.add(logistics)
    await db.commit()
    await db.refresh(logistics)
    order = await db.get(Order, order_id)
    if order:
        order.status = "DISPATCHED"
        db.add(order)
        await db.commit()
    return logistics

async def update_logistics(db: AsyncSession, order_id, payload):
    result = await db.execute(select(Logistics).where(Logistics.order_id == order_id))
    logistics = result.scalars().first()
    if not logistics:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(logistics, field, value)
    db.add(logistics)
    await db.commit()
    await db.refresh(logistics)
    return logistics

async def get_logistics(db: AsyncSession, order_id):
    result = await db.execute(select(Logistics).where(Logistics.order_id == order_id))
    return result.scalars().first()
