import uuid
from sqlalchemy import String, Column, ForeignKey, Integer, Numeric, DateTime
from app.core.types import GUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CashoutRequest(Base):
    __tablename__ = "cashout_requests"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    points_amount = Column(Integer, nullable=False)
    naira_value = Column(Numeric(12, 2), nullable=False)
    channel = Column(String(32), nullable=False)
    destination = Column(String(128), nullable=False)
    status = Column(String(32), nullable=False, default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="cashouts")
