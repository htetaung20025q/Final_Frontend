import asyncio
from config.database import SessionLocal
from schemas.user import UserLogin
from services.db_auth import login

async def test():
    async with SessionLocal() as session:
        user = UserLogin(email="admin@example.com", password="admin123")
        try:
            res = await login(user, session)
            print("Login success:", res)
        except Exception as e:
            print("Login failed with exception:", repr(e))

asyncio.run(test())
