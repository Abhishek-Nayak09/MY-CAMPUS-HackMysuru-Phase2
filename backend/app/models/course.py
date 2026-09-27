from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )