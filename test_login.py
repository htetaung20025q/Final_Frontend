import asyncio
from config.database import SessionLocal
from models.user_model import User
from sqlalchemy.future import select
from services.jwt_ser import verify_password

async def test():
    async with SessionLocal() as session:
        stmt = select(User).where(User.email == "admin@example.com")
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user:
            print(f"User found: {user.email}")
            print(f"Hashed password in DB: {user.hashed_password}")
            is_valid = verify_password("admin123", user.hashed_password)
            print(f"Password is valid: {is_valid}")
        else:
            print("User not found!")

asyncio.run(test())
