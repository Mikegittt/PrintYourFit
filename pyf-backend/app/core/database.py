from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url
from app.core.config import settings

raw_db_url = str(settings.DATABASE_URL)
url = make_url(raw_db_url)
db_url = raw_db_url
connect_args = {}

# SQLite async engine needs check_same_thread disabled for multiple callers
if url.drivername.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# No Neon-specific asyncpg normalization — use DATABASE_URL as provided

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
