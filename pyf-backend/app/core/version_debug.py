import platform
import sqlalchemy


def get_versions():
    return {
        "python": platform.python_version(),
        "sqlalchemy": sqlalchemy.__version__,
    }
