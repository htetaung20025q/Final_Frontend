from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import Product
from schemas.products import ProductCreate, ProductUpdate, ProductDelete
from fastapi import HTTPException


async def create(product_data: ProductCreate, db: AsyncSession):
    stmt = select(Product).filter(Product.name == product_data.name)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id,
        image_url=product_data.image_url,
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return {
        "Message": "Product created successfully", 
        "Data": {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price,
            "stock": new_product.stock,
            "image_url": new_product.image_url
        }
    }


async def get_products(category_id: int | None, min_price: int | None, max_price: int | None, available: bool | None, db: AsyncSession):
    stmt = select(Product)
    if category_id is not None:
        stmt = stmt.filter(Product.category_id == category_id)
    if min_price is not None:
        stmt = stmt.filter(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.filter(Product.price <= max_price)
    if available:
        stmt = stmt.filter(Product.stock > 0)
    
    result = await db.execute(stmt)
    products = result.scalars().all()
    return products


async def get_all_products(db: AsyncSession):
    stmt = select(Product)
    result = await db.execute(stmt)
    products = result.scalars().all()
    return products


async def update(product_data: ProductUpdate, db: AsyncSession):
    stmt = select(Product).filter(Product.id == product_data.id)
    result = await db.execute(stmt)
    db_product = result.scalars().first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        db_product.name = product_data.name
        db_product.description = product_data.description
        db_product.price = product_data.price
        db_product.stock = product_data.stock
        db_product.category_id = product_data.category_id
        
        if product_data.image_url is not None:
            db_product.image_url = product_data.image_url

        await db.commit()
        await db.refresh(db_product)
        return {"Message": "Product updated successfully"}


async def delete(product_id: int, db: AsyncSession):
    stmt = select(Product).filter(Product.id == product_id)
    result = await db.execute(stmt)
    db_product = result.scalars().first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        await db.delete(db_product)
        await db.commit()
        return {"message": "Product deleted successfully"}
