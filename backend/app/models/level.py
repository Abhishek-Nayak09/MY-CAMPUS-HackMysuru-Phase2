from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Level(Base):
    __tablename__ = "levels"

    __table_args__ = (
        UniqueConstraint(
            "subject_id",
            "level_order",
            name="uq_subject_level_order"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    level_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False
    )

    is_default_unlocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    unlock_score_required: Mapped[int] = mapped_column(
        Integer,
        default=8,
        nullable=False
    )