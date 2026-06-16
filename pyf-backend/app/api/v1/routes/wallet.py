from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import get_db, get_current_active_user
from app.services.points_service import get_user_points_balance, get_wallet_history
from app.services.cashout_service import create_cashout_request, get_cashout_history
from app.schemas.points import PointsBalanceResponse, WalletHistoryResponse
from app.schemas.cashout import CashoutRequestCreate, CashoutHistoryResponse

router = APIRouter()

@router.get("/balance", response_model=PointsBalanceResponse)
async def balance(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if db is None:
        return {"points": 0, "naira_value": 0.0}
    points = await get_user_points_balance(db, current_user.id)
    return {"points": points, "naira_value": float(points * 10)}

@router.get("/history", response_model=WalletHistoryResponse)
async def history(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if db is None:
        return {"items": []}
    items = await get_wallet_history(db, current_user.id)
    return {"items": items}

@router.post("/cashout", response_model=CashoutHistoryResponse)
async def cashout(payload: CashoutRequestCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if db is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
    if payload.points_amount < 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Minimum cashout is 100 points")
    await create_cashout_request(db, current_user.id, payload)
    items = await get_cashout_history(db, current_user.id)
    return {"items": items}

@router.get("/cashout-history", response_model=CashoutHistoryResponse)
async def cashout_history(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if db is None:
        return {"items": []}
    items = await get_cashout_history(db, current_user.id)
    return {"items": items}
