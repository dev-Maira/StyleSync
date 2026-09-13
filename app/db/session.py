from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# 1. Async Engine banao (joins FastAPI to Postgres via asyncpg)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True  # Terminal par SQL queries print hone ke liye
)

# 2. Async Session factory setup karo
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. Dependency function jo FastAPI endpoints ko DB session dega
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session