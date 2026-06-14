from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class OrderCreate(BaseModel):
    product_type: str
    description: Optional[str] = None
    quantity: int
    file_url: Optional[str] = None
    design_prompt: Optional[str] = None
    unit_price: float
    delivery_address: str
    delivery_fee: float
    referred_by: Optional[UUID] = None

class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    print_shop_id: UUID
    referred_by: Optional[UUID] = None
    product_type: str
    description: Optional[str] = None
    quantity: int
    file_url: Optional[str] = None
    design_prompt: Optional[str] = None
    unit_price: float
    total_price: float
    status: str
    delivery_address: str
    delivery_fee: float
    payment_reference: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str

class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
