from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Topic(Base):
    __tablename__ = "topics"

    __table_args__ = (
        UniqueConstraint(
            "level_id",
            "topic_order",
            name="uq_level_topic_order"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    topic_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False
    )

    level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id"),
        nullable=False
    )

    visualization_type: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    game_type: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )