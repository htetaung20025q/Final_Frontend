from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://htetagg:password123@localhost/finalproject"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
