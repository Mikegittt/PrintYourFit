from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.points_ledger import PointsLedger
from app.models.order import Order
from app.models.user import User
from decimal import Decimal

POINT_VALUE = Decimal("10")
COMMISION_RATE = Decimal("0.05")

async def get_user_points_balance(db: AsyncSession, user_id):
    result = await db.execute(
        select(func.coalesce(func.sum(PointsLedger.points_delta), 0))
        .where(PointsLedger.user_id == user_id)
    )
    points = result.scalar_one()
    return int(points)

async def get_wallet_history(db: AsyncSession, user_id, limit: int = 50, offset: int = 0):
    result = await db.execute(
        select(PointsLedger)
        .where(PointsLedger.user_id == user_id)
        .order_by(PointsLedger.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()

async def credit_commission(db: AsyncSession, order: Order):
    if not order.referred_by or order.status != "PAID":
        return
    points = int((order.total_price * COMMISION_RATE) / POINT_VALUE)
    fiat_equivalent = Decimal(points) * POINT_VALUE
    ledger = PointsLedger(
        user_id=order.referred_by,
        points_delta=points,
        fiat_equivalent=fiat_equivalent,
        transaction_type="COMMISSION",
        order_id=order.id,
    )
    db.add(ledger)
    await db.commit()
    await db.refresh(ledger)
    return ledger
