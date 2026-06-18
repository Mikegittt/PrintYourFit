from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url
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
    logger.info(f"[DATABASE] Using {url.drivername}: {raw_db_url}")
    db_url = raw_db_url
    # For PostgreSQL and other databases, don't set check_same_thread

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
