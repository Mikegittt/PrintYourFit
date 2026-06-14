import uuid
from sqlalchemy import Integer, Column, ForeignKey, Numeric, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PointsLedger(Base):
    __tablename__ = "points_ledger"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    points_delta = Column(Integer, nullable=False)
    fiat_equivalent = Column(Numeric(12, 2), nullable=False)
    transaction_type = Column(String(32), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="points")
    order = relationship("Order", back_populates="points")
