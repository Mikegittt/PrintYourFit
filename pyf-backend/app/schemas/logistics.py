from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class LogisticsCreate(BaseModel):
    dispatcher_name: str
    tracking_notes: str
    estimated_delivery: Optional[str] = None

class LogisticsUpdate(BaseModel):
    dispatcher_name: Optional[str] = None
    tracking_notes: Optional[str] = None
    dispatched_at: Optional[str] = None
    estimated_delivery: Optional[str] = None
    delivered_at: Optional[str] = None

class LogisticsResponse(BaseModel):
    id: UUID
    order_id: UUID
    dispatcher_name: Optional[str] = None
    tracking_notes: Optional[str] = None
    dispatched_at: Optional[str] = None
    estimated_delivery: Optional[str] = None
    delivered_at: Optional[str] = None

    class Config:
        from_attributes = True
