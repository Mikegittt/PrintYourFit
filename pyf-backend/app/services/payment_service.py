import uuid
import httpx
from app.core.config import settings
from app.models.order import Order
from app.models.print_shop import PrintShop
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

async def initiate_paystack_payment(order: Order, db: AsyncSession) -> dict:
    customer = await db.get(User, order.customer_id)
    payload = {
        "amount": int((order.total_price + Decimal(order.delivery_fee)) * 100),
        "email": customer.email if customer else None,
        "reference": str(order.id),
        "callback_url": "",
        "metadata": {
            "order_id": str(order.id),
        },
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.PAYSTACK_BASE_URL}/transaction/initialize",
            headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("data", {})

async def verify_paystack_payment(reference: str, db: AsyncSession) -> Order | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}",
            headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json().get("data", {})
    if data.get("status") == "success":
        result = await db.execute(select(Order).where(Order.id == reference))
        return result.scalars().first()
    return None

async def initiate_paystack_onboarding(user: User, payload: dict) -> dict:
    reference = str(uuid.uuid4())
    amount = settings.PRINT_SHOP_ONBOARDING_FEE_NAIRA * 100
    metadata = {
        "user_id": str(user.id),
        "shop_name": payload.get("shop_name"),
        "address": payload.get("address"),
        "state": payload.get("state"),
        "phone": payload.get("phone"),
    }
    payload_data = {
        "amount": amount,
        "email": user.email,
        "reference": reference,
        "callback_url": f"{settings.FRONTEND_URL}/shop/onboard/verify",
        "metadata": metadata,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.PAYSTACK_BASE_URL}/transaction/initialize",
            headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
            json=payload_data,
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("data", {})

async def verify_paystack_onboarding(reference: str, db: AsyncSession, user: User) -> PrintShop | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}",
            headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json().get("data", {})

    if data.get("status") == "success":
        metadata = data.get("metadata", {})
        if metadata.get("user_id") != str(user.id):
            return None

        result = await db.execute(select(PrintShop).where(PrintShop.user_id == user.id))
        existing_shop = result.scalars().first()
        if existing_shop:
            return existing_shop

        shop = PrintShop(
            user_id=user.id,
            shop_name=metadata.get("shop_name"),
            address=metadata.get("address"),
            state=metadata.get("state"),
            is_verified=False,
        )
        db.add(shop)
        await db.commit()
        await db.refresh(shop)
        return shop
    return None
