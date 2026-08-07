from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    stock: int
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int


class ProductDelete(BaseModel):
    id: int

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
