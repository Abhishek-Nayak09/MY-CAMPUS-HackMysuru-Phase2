import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================================================
# DATABASE PATH
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parents[2]

LOCAL_DATABASE_FILE = (
    BACKEND_DIR
    / "learning.db"
)


# =========================================================
# DATABASE URL
#
# LOCAL:
#   No DATABASE_URL environment variable
#   -> uses existing backend/learning.db
#
# DEPLOYED:
#   DATABASE_URL environment variable exists
#   -> uses hosted PostgreSQL
# =========================================================

ENV_DATABASE_URL = (
    os.getenv(
        "DATABASE_URL"
    )
    or ""
).strip()


if ENV_DATABASE_URL:

    # Some hosting providers may still return
    # postgres:// instead of postgresql://.
    if ENV_DATABASE_URL.startswith(
        "postgres://"
    ):

        ENV_DATABASE_URL = (
            "postgresql://"
            +
            ENV_DATABASE_URL[
                len("postgres://"):
            ]
        )


    DATABASE_URL = (
        ENV_DATABASE_URL
    )

    USING_SQLITE = False

else:

    DATABASE_URL = (
        f"sqlite:///"
        f"{LOCAL_DATABASE_FILE.as_posix()}"
    )

    USING_SQLITE = True


# =========================================================
# DATABASE ENGINE
# =========================================================

if USING_SQLITE:

    engine = create_engine(

        DATABASE_URL,

        connect_args={
            "check_same_thread":
                False
        },

        pool_pre_ping=True,
    )

else:

    engine = create_engine(

        DATABASE_URL,

        pool_pre_ping=True,
    )


# =========================================================
# DATABASE SESSION
# =========================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine,
)


# =========================================================
# BASE MODEL
# =========================================================

Base = declarative_base()


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()