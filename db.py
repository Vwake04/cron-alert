import os
from models import Upgrade  # noqa
from sqlmodel import Session  # noqa
from sqlmodel import SQLModel, create_engine
from urllib.parse import quote_plus


def get_database_url():
    """Get database URL from environment variables with fallback to SQLite."""
    db_type = os.getenv("DB_TYPE", "sqlite").lower()

    if db_type == "sqlite":
        db_path = os.getenv("DB_PATH", "db.sqlite3")
        return f"sqlite:///{db_path}"

    elif db_type == "postgresql":
        user = os.getenv("DB_USER", "postgres")
        password = quote_plus(os.getenv("DB_PASSWORD", ""))
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        database = os.getenv("DB_NAME", "upgrades")
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def init_db(database_url: str = None):
    if not database_url:
        database_url = get_database_url()

    # Configure SQLAlchemy engine
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    engine = create_engine(
        database_url,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true",
        connect_args=connect_args,
    )

    SQLModel.metadata.create_all(engine)
    return engine
