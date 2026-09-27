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


# =========================================================
# NOTE
# One complete note package for one topic
# =========================================================

class Note(Base):

    __tablename__ = "notes"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    # Topic this note belongs to
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False,
        index=True
    )


    # Faculty who created/uploaded it
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )


    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


    subtitle: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True
    )


    introduction: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    # Downloadable faculty PDF
    pdf_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# =========================================================
# NOTE SECTION
#
# Each note is made from multiple sections.
#
# Supported section_type examples:
#
# story
# concept
# definition
# real_world
# application
# image
# animation
# diagram
# example
# checkpoint
# summary
# =========================================================

class NoteSection(Base):

    __tablename__ = "note_sections"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id"),
        nullable=False,
        index=True
    )


    section_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    section_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    heading: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )


    # Main explanation / story / example text
    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    # Image, GIF, SVG or other media path
    media_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    media_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    # Examples:
    # image
    # gif
    # svg
    # animation


    caption: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    alt_text: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True
    )


    # Flexible data for checkpoints or interactive sections.
    #
    # Example:
    # {
    #   "question": "...",
    #   "options": [...],
    #   "answer": "..."
    # }
    #
    # Stored as JSON text for now.
    interactive_data: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )