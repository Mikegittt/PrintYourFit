from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cashout_request import CashoutRequest
from app.models.points_ledger import PointsLedger
from decimal import Decimal
from sqlalchemy import select, func

async def create_cashout_request(db: AsyncSession, user_id, request_data):
    cashout = CashoutRequest(
        user_id=user_id,
        points_amount=request_data.points_amount,
        naira_value=Decimal(request_data.naira_value),
        channel=request_data.channel,
        destination=request_data.destination,
    )
    db.add(cashout)
    await db.commit()
    await db.refresh(cashout)
    ledger = PointsLedger(
        user_id=user_id,
        points_delta=-request_data.points_amount,
        fiat_equivalent=Decimal(request_data.naira_value),
        transaction_type="CASH_OUT",
        order_id=None,
    )
    db.add(ledger)
    await db.commit()
    return cashout

async def get_cashout_history(db: AsyncSession, user_id):
    result = await db.execute(select(CashoutRequest).where(CashoutRequest.user_id == user_id).order_by(CashoutRequest.created_at.desc()))
    return result.scalars().all()
