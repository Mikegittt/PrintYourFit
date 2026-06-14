from pydantic import BaseModel
from uuid import UUID

class PointsBalanceResponse(BaseModel):
    points: int
    naira_value: float

class PointsLedgerItem(BaseModel):
    id: int
    points_delta: int
    fiat_equivalent: float
    transaction_type: str
    order_id: UUID | None = None
    created_at: str

    class Config:
        from_attributes = True

class WalletHistoryResponse(BaseModel):
    items: list[PointsLedgerItem]
