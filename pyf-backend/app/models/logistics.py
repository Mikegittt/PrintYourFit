import uuid
from sqlalchemy import Column, ForeignKey, String, Text, DateTime
from app.core.types import GUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Logistics(Base):
    __tablename__ = "logistics"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=False)
    dispatcher_name = Column(String(128), nullable=True)
    tracking_notes = Column(Text, nullable=True)
    dispatched_at = Column(DateTime(timezone=True), nullable=True)
    estimated_delivery = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    order = relationship("Order", back_populates="logistics")
