from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Table,
    Enum,
)

from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class OrderStatus(PyEnum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"


order_items = Table(
    "order_items",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1),
    Column("unit_price", Integer, nullable=False),
)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Integer, nullable=False, default=0)
    # store status as a string to avoid dialect-specific Enum binding issues
    status = Column(String(20), nullable=False, default=OrderStatus.pending.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary=order_items, back_populates="orders")
