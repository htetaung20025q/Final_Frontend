from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import Product
from models.product_model import Order, order_items, OrderStatus
from fastapi import HTTPException


async def place_order(order_data, db: AsyncSession):
    if not order_data.items:
        raise HTTPException(status_code=400, detail="No items provided")

    total_price = 0

    new_order = Order(user_id=order_data.user_id, total_price=0)
    db.add(new_order)
    await db.flush()

    for item in order_data.items:
        stmt = select(Product).filter(Product.id == item.product_id)
        result = await db.execute(stmt)
        product = result.scalars().first()
        if product is None:
            raise HTTPException(
                status_code=404, detail=f"Product {item.product_id} not found"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400, detail=f"Insufficient stock for product {product.id}"
            )

        unit_price = product.price
        line_total = unit_price * item.quantity
        total_price += line_total

        product.stock = product.stock - item.quantity

        await db.execute(
            order_items.insert().values(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=unit_price,
            )
        )

    new_order.total_price = total_price
    await db.commit()
    await db.refresh(new_order)

    return {"message": "Order placed successfully", "order": new_order}


async def update_order_status(order_id: int, status_str: str, db: AsyncSession):
    stmt = select(Order).filter(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalars().first()
    
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        new_status = OrderStatus(status_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status value")

    order.status = new_status.value
    await db.commit()
    await db.refresh(order)

    return {"message": "Order status updated", "order": order}


async def get_order(order_id: int, db: AsyncSession):
    stmt = select(Order).filter(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalars().first()
    
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    rows_result = await db.execute(order_items.select().where(order_items.c.order_id == order_id))
    rows = rows_result.mappings().all()

    items = []
    for r in rows:
        prod_stmt = select(Product).filter(Product.id == r["product_id"])
        prod_result = await db.execute(prod_stmt)
        product = prod_result.scalars().first()
        if product:
            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                },
                "quantity": r["quantity"],
                "unit_price": r["unit_price"],
                "line_total": r["quantity"] * r["unit_price"],
            }
            items.append(item)

    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_price": order.total_price,
        "status": order.status,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "items": items,
    }


async def get_user_orders(user_id: int, db: AsyncSession):
    stmt = select(Order).filter(Order.user_id == user_id)
    result = await db.execute(stmt)
    orders = result.scalars().all()
    return orders

async def get_all_orders(db: AsyncSession):
    stmt = select(Order)
    result = await db.execute(stmt)
    orders = result.scalars().all()
    return orders
