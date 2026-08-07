from pydantic import BaseModel
from typing import List


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class PlaceOrderRequest(BaseModel):
    user_id: int
    items: List[OrderItem]


class OrderStatusUpdate(BaseModel):
    status: str
