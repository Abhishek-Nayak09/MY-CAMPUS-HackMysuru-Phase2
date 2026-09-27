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


class DoubtTicket(Base):

    __tablename__ = "doubt_tickets"


    # =========================================================
    # PRIMARY KEY
    # =========================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    # =========================================================
    # STUDENT
    # =========================================================

    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )


    # =========================================================
    # LEARNING CONTEXT
    # =========================================================

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False
    )


    level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id"),
        nullable=False
    )


    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False
    )


    # =========================================================
    # STUDENT PROBLEM
    # =========================================================

    doubt_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    weak_concept: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )


    attempted_methods: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    ai_attempted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )


    # =========================================================
    # FACULTY ASSIGNMENT
    # =========================================================

    assigned_faculty_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )


    faculty_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    # =========================================================
    # STATUS
    # =========================================================

    status: Mapped[str] = mapped_column(
        String(30),
        default="new",
        nullable=False,
        index=True
    )


    # =========================================================
    # TIME TRACKING
    # =========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )