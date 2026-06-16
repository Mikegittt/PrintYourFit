from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url
from app.core.config import settings

DEFAULT_SQLITE_URL = "sqlite+aiosqlite:///./dev.db"
raw_db_url = str(settings.DATABASE_URL).strip()
connect_args = {}

try:
    url = make_url(raw_db_url)
except Exception:
    url = make_url(DEFAULT_SQLITE_URL)
    raw_db_url = DEFAULT_SQLITE_URL

if not url.drivername.startswith("sqlite"):
    print(
        "WARNING: DATABASE_URL is not SQLite. Falling back to local SQLite for runtime."
    )
    db_url = DEFAULT_SQLITE_URL
    connect_args["check_same_thread"] = False
else:
    db_url = raw_db_url
    connect_args["check_same_thread"] = False

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
