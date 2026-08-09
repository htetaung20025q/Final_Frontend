import asyncio
from config.database import SessionLocal
from schemas.products import ProductCreate
from services.product_service import create

async def test():
    async with SessionLocal() as db:
        product = ProductCreate(
            name="Shirt",
            description="Clothing",
            price=50000,
            stock=50,
            category_id=1
        )
        try:
            res = await create(product, db)
            print("Create success:", res)
        except Exception as e:
            print("Create failed with exception:", repr(e))

asyncio.run(test())
