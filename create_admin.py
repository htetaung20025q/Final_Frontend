import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.user_model import User
from config.database import DATABASE_URL
from services.jwt_ser import hash_password

async def create_admin():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        from sqlalchemy.future import select
        stmt = select(User).filter(User.username == "admin")
        result = await session.execute(stmt)
        admin_user = result.scalars().first()
        
        if admin_user:
            print("Admin user already exists! Username: admin")
        else:
            hashed = hash_password("admin123")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=hashed,
                is_admin=True,
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Email: admin@example.com")
            print("Password: admin123")
            print("You can use this to login to the Admin Dashboard.")

if __name__ == "__main__":
    asyncio.run(create_admin())
