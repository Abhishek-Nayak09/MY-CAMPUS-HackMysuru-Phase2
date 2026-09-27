
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
)

from app.db.database import Base


# ============================================================
# STUDENT LEARNING PROFILE
# ============================================================

class StudentLearningProfile(Base):

    __tablename__ = "student_learning_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        unique=True,
        nullable=False,
        index=True
    )

    # --------------------------------------------------------
    # ATTEMPTS BY LEARNING MODE
    # --------------------------------------------------------

    notes_attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

    video_attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

    interactive_attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

    game_attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

    ai_tutor_attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

    faculty_attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

    # --------------------------------------------------------
    # SUCCESS / UNDERSTANDING BY LEARNING MODE
    # --------------------------------------------------------

    notes_understood = Column(
        Integer,
        default=0,
        nullable=False
    )

    video_understood = Column(
        Integer,
        default=0,
        nullable=False
    )

    interactive_understood = Column(
        Integer,
        default=0,
        nullable=False
    )

    game_understood = Column(
        Integer,
        default=0,
        nullable=False
    )

    ai_tutor_understood = Column(
        Integer,
        default=0,
        nullable=False
    )

    faculty_resolved = Column(
        Integer,
        default=0,
        nullable=False
    )

    topics_understood = Column(
        Integer,
        default=0,
        nullable=False
    )

    faculty_escalations = Column(
        Integer,
        default=0,
        nullable=False
    )

    preferred_resource = Column(
        String(32),
        nullable=True
    )

    last_successful_resource = Column(
        String(32),
        nullable=True
    )

    preference_confidence = Column(
        Float,
        default=0.0,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# ============================================================
# PER-TOPIC RESOURCE PROGRESS
# ============================================================

class StudentTopicResourceProgress(Base):

    __tablename__ = "student_topic_resource_progress"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "topic_id",
            "resource_type",
            name="uq_student_topic_resource"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    topic_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    resource_type = Column(
        String(32),
        nullable=False,
        index=True
    )

    status = Column(
        String(32),
        default="not_started",
        nullable=False
    )

    visit_count = Column(
        Integer,
        default=0,
        nullable=False
    )

    understood_here = Column(
        Boolean,
        default=False,
        nullable=False
    )

    started_at = Column(
        DateTime,
        nullable=True
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    understood_at = Column(
        DateTime,
        nullable=True
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# ============================================================
# TOPIC JOURNEY
# ============================================================

class StudentTopicJourney(Base):

    __tablename__ = "student_topic_journeys"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "topic_id",
            name="uq_student_topic_journey"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    topic_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    current_resource = Column(
        String(32),
        default="notes",
        nullable=False
    )

    resolved = Column(
        Boolean,
        default=False,
        nullable=False
    )

    resolved_resource = Column(
        String(32),
        nullable=True
    )

    started_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    resolved_at = Column(
        DateTime,
        nullable=True
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
