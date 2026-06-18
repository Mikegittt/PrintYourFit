from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

DEFAULT_SQLITE_URL = "sqlite+aiosqlite:///./dev.db"
raw_db_url = str(settings.DATABASE_URL).strip()
connect_args = {}

try:
    url = make_url(raw_db_url)
except Exception as e:
    logger.warning(f"[DATABASE] Failed to parse DATABASE_URL: {e}. Using SQLite.")
    url = make_url(DEFAULT_SQLITE_URL)
    raw_db_url = DEFAULT_SQLITE_URL

# Use the provided database URL if it's valid, otherwise fall back to SQLite
if url.drivername.startswith("sqlite"):
    logger.info(f"[DATABASE] Using SQLite: {raw_db_url}")
    db_url = raw_db_url
    connect_args["check_same_thread"] = False
else:
    # For PostgreSQL with asyncpg, we need to:
    # 1. Convert postgresql:// to postgresql+asyncpg:// for async support
    # 2. Remove query parameters incompatible with asyncpg (like sslmode)
    logger.info(f"[DATABASE] Using PostgreSQL with asyncpg: {raw_db_url}")
    
    # Replace postgresql:// with postgresql+asyncpg://
    if raw_db_url.startswith("postgresql://"):
        raw_db_url = raw_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    
    # Re-parse the modified URL
    url = make_url(raw_db_url)
    
    # Remove sslmode and other incompatible parameters
    if url.query:
        filtered_query = {
            k: v
            for k, v in url.query.items()
            if k.lower() not in ['sslmode', 'channel_binding']
        }
        if filtered_query:
            db_url = str(url.set(query=filtered_query))
        else:
            db_url = str(url.set(query={}))
    else:
        db_url = raw_db_url
    
    logger.info(f"[DATABASE] Final URL scheme: {url.drivername}")

engine: AsyncEngine = create_async_engine(
    db_url,
    future=True,
    echo=False,
    connect_args=connect_args,
    poolclass=NullPool if not url.drivername.startswith("sqlite") else None,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# Ensure all models are imported so SQLAlchemy Base metadata is populated
# when `create_all` is called from tests or external scripts.
try:
    import app.models  # noqa: F401
except Exception:
    # Import errors should not prevent module import; they'll surface later
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
