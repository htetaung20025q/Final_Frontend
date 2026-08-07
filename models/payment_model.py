from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class PaymentStatus(PyEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default=PaymentStatus.pending.value)
    transaction_id = Column(String(100), nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order")
