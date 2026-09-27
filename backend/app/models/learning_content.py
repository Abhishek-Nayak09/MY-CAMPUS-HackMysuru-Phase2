from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class LearningContent(Base):

    __tablename__ = "learning_contents"


    # =========================================================
    # PRIMARY KEY
    # =========================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    # =========================================================
    # TOPIC
    # =========================================================

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False,
        index=True
    )


    # =========================================================
    # CONTENT TYPE
    # =========================================================

    resource_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    # Expected:
    # notes
    # video
    # visualization
    # game


    # =========================================================
    # CONTENT DETAILS
    # =========================================================

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    content_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    resource_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    # =========================================================
    # DISPLAY ORDER
    # =========================================================

    content_order: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )


    # =========================================================
    # FACULTY SOURCE
    # =========================================================

    uploaded_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )


    # =========================================================
    # STATUS
    # =========================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )


    # =========================================================
    # CREATED TIME
    # =========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )