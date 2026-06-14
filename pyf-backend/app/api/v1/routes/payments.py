from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import get_db, get_current_active_user
from app.services.payment_service import (
    initiate_paystack_payment,
    verify_paystack_payment,
    initiate_paystack_onboarding,
    verify_paystack_onboarding,
)
from app.services.points_service import credit_commission
from app.models.order import Order
from app.models.user import User

router = APIRouter()

@router.post("/initiate")
async def initiate_payment(order_id: str, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    payment_data = await initiate_paystack_payment(order, db)
    return payment_data

@router.post("/verify")
async def verify_payment(reference: str, db: AsyncSession = Depends(get_db)):
    order = await verify_paystack_payment(reference, db)
    if not order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not verify payment")
    order.status = "PAID"
    order.payment_reference = reference
    db.add(order)
    await db.commit()
    await credit_commission(db, order)
    return {"status": "paid", "order_id": str(order.id)}

@router.post("/onboard-shop")
async def onboard_print_shop(payload: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "PRINT_SHOP":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only print shop users can onboard shops")
    payment_data = await initiate_paystack_onboarding(current_user, payload)
    return payment_data

@router.post("/verify-onboarding")
async def verify_print_shop_onboarding(reference: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "PRINT_SHOP":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only print shop users can verify onboarding")
    shop = await verify_paystack_onboarding(reference, db, current_user)
    if not shop:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not verify onboarding payment")
    return {"status": "paid", "shop_id": str(shop.id)}
