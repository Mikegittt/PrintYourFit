import uuid
from sqlalchemy import String, Column, Text, DateTime, LargeBinary
from app.core.types import GUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Design(Base):
    __tablename__ = "designs"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    image_url = Column(String(512), nullable=True)  # URL or base64
    image_data = Column(LargeBinary, nullable=True)  # stored binary image
    format = Column(String(32), default="PNG")  # PNG, SVG, JPEG, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
