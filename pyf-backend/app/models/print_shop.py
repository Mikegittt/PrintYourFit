import uuid
from sqlalchemy import String, Column, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PrintShop(Base):
    __tablename__ = "print_shops"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    shop_name = Column(String(128), nullable=False)
    address = Column(Text, nullable=False)
    state = Column(String(64), nullable=False)
    status = Column(String(32), default="PENDING")  # PENDING, APPROVED, REJECTED
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="print_shop")
    orders = relationship("Order", back_populates="print_shop")
