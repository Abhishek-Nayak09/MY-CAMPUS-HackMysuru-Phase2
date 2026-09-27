from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================================================
# DATABASE PATH
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parents[2]

DATABASE_FILE = BACKEND_DIR / "learning.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
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