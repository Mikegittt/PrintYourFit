from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import get_db, require_role
from app.services.logistics_service import create_dispatch, update_logistics, get_logistics
from app.schemas.logistics import LogisticsCreate, LogisticsUpdate, LogisticsResponse

router = APIRouter()

@router.post("/{order_id}/dispatch", response_model=LogisticsResponse, dependencies=[Depends(require_role("ADMIN"))])
async def dispatch(order_id: str, payload: LogisticsCreate, db: AsyncSession = Depends(get_db)):
    logistics = await create_dispatch(db, order_id, payload)
    if not logistics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return logistics

@router.put("/{order_id}/update", response_model=LogisticsResponse, dependencies=[Depends(require_role("ADMIN"))])
async def update(order_id: str, payload: LogisticsUpdate, db: AsyncSession = Depends(get_db)):
    logistics = await update_logistics(db, order_id, payload)
    if not logistics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logistics record not found")
    return logistics

@router.get("/{order_id}", response_model=LogisticsResponse, dependencies=[Depends(require_role("ADMIN"))])
async def fetch(order_id: str, db: AsyncSession = Depends(get_db)):
    logistics = await get_logistics(db, order_id)
    if not logistics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logistics record not found")
    return logistics
