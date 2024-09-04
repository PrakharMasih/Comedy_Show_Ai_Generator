from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Use aiosqlite for async SQLite support
DB_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    DB_URL, echo=True
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db