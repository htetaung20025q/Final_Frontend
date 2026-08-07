import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from config.database import DATABASE_URL

async def add_column():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE products ADD COLUMN category_id INTEGER;"))
            print("Successfully added category_id column to products table!")
        except Exception as e:
            print(f"Could not add column (it may already exist): {e}")

if __name__ == "__main__":
    asyncio.run(add_column())
