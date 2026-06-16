import platform
import sqlalchemy
import asyncpg


def get_versions():
    return {
        "python": platform.python_version(),
        "sqlalchemy": sqlalchemy.__version__,
        "asyncpg": asyncpg.__version__,
    }
