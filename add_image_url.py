import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from config.database import DATABASE_URL

async def add_image_url():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE products ADD COLUMN image_url VARCHAR(255);"))
            print("Added image_url column")
        except Exception as e:
            print("Failed:", e)

asyncio.run(add_image_url())
