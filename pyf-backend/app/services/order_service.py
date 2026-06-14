from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order
from app.models.print_shop import PrintShop
from app.schemas.order import OrderCreate
from decimal import Decimal
from app.core.config import settings

async def create_order(db: AsyncSession, customer_id, order_in: OrderCreate):
    print_shop_id = order_in.design_prompt and settings.DEFAULT_PRINT_SHOP_ID or settings.DEFAULT_PRINT_SHOP_ID
    order = Order(
        customer_id=customer_id,
        print_shop_id=print_shop_id,
        referred_by=order_in.referred_by,
        product_type=order_in.product_type,
        description=order_in.description,
        quantity=order_in.quantity,
        file_url=order_in.file_url,
        design_prompt=order_in.design_prompt,
        unit_price=Decimal(order_in.unit_price),
        delivery_address=order_in.delivery_address,
        delivery_fee=Decimal(order_in.delivery_fee),
        total_price=Decimal(order_in.unit_price) * order_in.quantity + Decimal(order_in.delivery_fee),
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def get_order_by_id(db: AsyncSession, order_id):
    return await db.get(Order, order_id)

async def update_order_status(db: AsyncSession, order: Order, status: str):
    order.status = status
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def list_shop_orders(db: AsyncSession, shop_id):
    result = await db.execute(select(Order).where(Order.print_shop_id == shop_id).order_by(Order.created_at.desc()))
    return result.scalars().all()

async def list_user_orders(db: AsyncSession, customer_id):
    result = await db.execute(select(Order).where(Order.customer_id == customer_id).order_by(Order.created_at.desc()))
    return result.scalars().all()

async def list_all_orders(db: AsyncSession):
    result = await db.execute(select(Order).order_by(Order.created_at.desc()))
    return result.scalars().all()
