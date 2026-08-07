from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.payment_model import Payment, PaymentStatus
from models.product_model import Order, OrderStatus
from schemas.payments import PaymentCreate, PaymentStatusUpdate
from fastapi import HTTPException
import uuid

async def process_payment(payment_data: PaymentCreate, db: AsyncSession):
    stmt = select(Order).filter(Order.id == payment_data.order_id)
    result = await db.execute(stmt)
    order = result.scalars().first()
    
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.total_price != payment_data.amount:
        raise HTTPException(status_code=400, detail="Payment amount does not match order total")

    # Simulate payment processing
    transaction_id = str(uuid.uuid4())

    new_payment = Payment(
        order_id=payment_data.order_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        status=PaymentStatus.completed.value,
        transaction_id=transaction_id
    )
    db.add(new_payment)
    
    # Update order status to paid
    order.status = OrderStatus.paid.value
    
    await db.commit()
    await db.refresh(new_payment)
    return new_payment

async def get_payment(payment_id: int, db: AsyncSession):
    stmt = select(Payment).filter(Payment.id == payment_id)
    result = await db.execute(stmt)
    payment = result.scalars().first()
    
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    return payment

async def update_payment_status(payment_id: int, status_data: PaymentStatusUpdate, db: AsyncSession):
    stmt = select(Payment).filter(Payment.id == payment_id)
    result = await db.execute(stmt)
    payment = result.scalars().first()
    
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    try:
        new_status = PaymentStatus(status_data.status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status value")

    payment.status = new_status.value
    if status_data.transaction_id:
        payment.transaction_id = status_data.transaction_id
        
    await db.commit()
    await db.refresh(payment)
    return payment
