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

# PostgreSQL asyncpg URLs should not pass unsupported query args directly into asyncpg
if url.drivername == "postgresql+asyncpg":
    query = dict(url.query)
    sslmode = query.pop("sslmode", None)
    if sslmode is not None:
        query["ssl"] = "true" if sslmode in ("require", "verify-ca", "verify-full") else "false"

    query.pop("channel_binding", None)

    ssl_value = query.get("ssl")
    if ssl_value in ("true", "1", "yes"):
        connect_args["ssl"] = True
    elif ssl_value in ("false", "0", "no"):
        connect_args["ssl"] = False

    db_url = str(url.set(query=query))

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
