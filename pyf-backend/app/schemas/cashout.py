from pydantic import BaseModel, Field
from uuid import UUID

class CashoutRequestCreate(BaseModel):
    points_amount: int
    naira_value: float
    channel: str
    destination: str

class CashoutResponse(BaseModel):
    id: UUID
    user_id: UUID
    points_amount: int
    naira_value: float
    channel: str
    destination: str
    status: str
    created_at: str

    class Config:
        from_attributes = True

class CashoutHistoryResponse(BaseModel):
    items: list[CashoutResponse]
