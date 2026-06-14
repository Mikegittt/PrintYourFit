from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DesignCreate(BaseModel):
    prompt: str

class DesignResponse(BaseModel):
    id: UUID
    user_id: UUID
    prompt: str
    image_url: Optional[str]
    format: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class DesignExport(BaseModel):
    design_id: str
    format: str  # PNG, SVG, JPEG, WebP

class SendToPrinter(BaseModel):
    design_id: str
    printer_id: Optional[str] = None
    printer_name: Optional[str] = None
