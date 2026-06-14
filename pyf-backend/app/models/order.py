import uuid
from sqlalchemy import String, Column, ForeignKey, Integer, Numeric, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    print_shop_id = Column(UUID(as_uuid=True), ForeignKey("print_shops.id"), nullable=False)
    referred_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    product_type = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=False)
    file_url = Column(Text, nullable=True)
    design_prompt = Column(Text, nullable=True)
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    status = Column(String(32), nullable=False, default="PENDING")
    delivery_address = Column(Text, nullable=False)
    delivery_fee = Column(Numeric(12, 2), nullable=False)
    payment_reference = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    customer = relationship("User", back_populates="orders", foreign_keys=[customer_id])
    print_shop = relationship("PrintShop", back_populates="orders")
    points = relationship("PointsLedger", back_populates="order")
    logistics = relationship("Logistics", back_populates="order", uselist=False)
