from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import re
import ssl
import asyncpg

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
    # Use an SSLContext instance for asyncpg
    connect_args["ssl"] = ssl.create_default_context()

# asyncpg versions older than what SQLAlchemy expects may error when SQLAlchemy
# passes `channel_binding`; create a small wrapper to remove that kwarg.
async def _asyncpg_connect_wrapper(*args, **kwargs):
    kwargs.pop("channel_binding", None)
    return await asyncpg.connect(*args, **kwargs)

# SQLAlchemy asyncpg dialect expects async_creator_fn, not creator
connect_args.setdefault("async_creator_fn", _asyncpg_connect_wrapper)

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
