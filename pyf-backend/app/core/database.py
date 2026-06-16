from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import re

# Normalize DATABASE_URL for asyncpg and handle SSL via connect_args
raw_db_url = str(settings.DATABASE_URL)
db_url = raw_db_url

# Ensure asyncpg driver in the scheme
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove psycopg-style sslmode query param (asyncpg doesn't accept sslmode)
connect_args = {}
if "sslmode=" in db_url:
    # remove '?sslmode=...' or '&sslmode=...'
    db_url = re.sub(r'([&?])sslmode=[^&]*', lambda m: m.group(1) if m.group(1) == '&' else '?', db_url)
    db_url = re.sub(r'[?&]$', '', db_url)
    connect_args["ssl"] = True

engine: AsyncEngine = create_async_engine(
    db_url,
    future=True,
    echo=False,
    connect_args=connect_args,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
