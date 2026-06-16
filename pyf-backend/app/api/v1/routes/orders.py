from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import get_db, get_current_active_user, require_role
from app.models.print_shop import PrintShop
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import create_order, get_order_by_id, update_order_status, list_shop_orders, list_user_orders, list_all_orders

router = APIRouter()

@router.post("/create", response_model=OrderResponse)
async def create_order_endpoint(payload: OrderCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if db is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
    if current_user.role != "CUSTOMER":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only customers can create orders")
    order = await create_order(db, current_user.id, payload)
    return order

@router.get("/my-orders", response_model=list[OrderResponse])
async def my_orders(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if db is None:
        return []
    return await list_user_orders(db, current_user.id)

@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if db is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if current_user.role not in ["ADMIN", "PRINT_SHOP"] and order.customer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return order

@router.put("/{order_id}/status", response_model=OrderResponse, dependencies=[Depends(require_role("PRINT_SHOP", "ADMIN"))])
async def change_status(order_id: str, payload: OrderStatusUpdate, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return await update_order_status(db, order, payload.status)

@router.get("/shop-queue", response_model=list[OrderResponse], dependencies=[Depends(require_role("PRINT_SHOP"))])
async def shop_queue(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if db is None:
        return []
    shop = await db.execute(select(PrintShop).where(PrintShop.user_id == current_user.id))
    shop = shop.scalars().first()
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Print shop not registered")
    return await list_shop_orders(db, shop.id)

@router.get("/all", response_model=list[OrderResponse], dependencies=[Depends(require_role("ADMIN"))])
async def all_orders(db: AsyncSession = Depends(get_db)):
    if db is None:
        return []
    return await list_all_orders(db)
