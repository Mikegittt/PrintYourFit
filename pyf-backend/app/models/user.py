import uuid
from sqlalchemy import String, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.order import Order

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(32), nullable=False)
    referral_code = Column(String(32), unique=True, nullable=True)
    referred_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    target_campus = Column(String(64), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    referred_users = relationship("User", remote_side=[id])
    print_shop = relationship("PrintShop", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="customer", foreign_keys=[Order.customer_id])
    points = relationship("PointsLedger", back_populates="user")
    cashouts = relationship("CashoutRequest", back_populates="user")
