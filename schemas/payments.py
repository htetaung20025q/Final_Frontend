from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    order_id: int
    amount: int
    payment_method: str

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: int
    payment_method: str
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentStatusUpdate(BaseModel):
    status: str
    transaction_id: Optional[str] = None
