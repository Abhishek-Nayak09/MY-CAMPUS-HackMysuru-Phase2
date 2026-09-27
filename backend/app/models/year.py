from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AcademicYear(Base):
    __tablename__ = "academic_years"

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "year_number",
            name="uq_course_academic_year"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    year_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )