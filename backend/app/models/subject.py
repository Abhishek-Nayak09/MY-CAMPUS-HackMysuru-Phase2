from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "year_id",
            "code",
            name="uq_course_year_subject"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )

    year_id: Mapped[int] = mapped_column(
        ForeignKey("academic_years.id"),
        nullable=False
    )