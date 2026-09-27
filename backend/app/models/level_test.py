from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.sql import func

from app.db.database import Base


# ============================================================
# 1. STUDENT LEVEL PROGRESS
# ============================================================

class StudentLevelProgress(Base):

    __tablename__ = "student_level_progress"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False,
        index=True
    )

    level_id = Column(
        Integer,
        ForeignKey("levels.id"),
        nullable=False,
        index=True
    )

    is_unlocked = Column(
        Boolean,
        default=False,
        nullable=False
    )

    best_score = Column(
        Integer,
        default=0,
        nullable=False
    )

    last_attempt_at = Column(
        DateTime,
        nullable=True
    )

    unlocked_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (

        UniqueConstraint(
            "user_id",
            "subject_id",
            "level_id",
            name="uq_student_subject_level_progress"
        ),

    )


# ============================================================
# 2. LEVEL UNLOCK TEST QUESTIONS
# ============================================================

class LevelTestQuestion(Base):

    __tablename__ = "level_test_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False,
        index=True
    )

    # Level whose concepts are being tested.
    #
    # Example:
    # Entry test -> source_level_id = Entry
    source_level_id = Column(
        Integer,
        ForeignKey("levels.id"),
        nullable=False,
        index=True
    )

    # Level that becomes unlocked after passing.
    #
    # Example:
    # Entry test -> target_level_id = Basics
    target_level_id = Column(
        Integer,
        ForeignKey("levels.id"),
        nullable=False,
        index=True
    )

    topic_id = Column(
        Integer,
        ForeignKey("topics.id"),
        nullable=False,
        index=True
    )

    question_order = Column(
        Integer,
        nullable=False
    )

    question_text = Column(
        Text,
        nullable=False
    )

    # Stored as JSON text.
    #
    # Example:
    # ["Option A", "Option B", "Option C", "Option D"]
    options_json = Column(
        Text,
        nullable=False
    )

    correct_answer = Column(
        Text,
        nullable=False
    )

    explanation = Column(
        Text,
        nullable=False
    )

    # Human-readable weakness label.
    #
    # Example:
    # "Speed vs Velocity"
    concept_gap = Column(
        String(255),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (

        UniqueConstraint(
            "subject_id",
            "source_level_id",
            "target_level_id",
            "question_order",
            name="uq_level_test_question_order"
        ),

    )


# ============================================================
# 3. TEST ATTEMPT
# ============================================================

class LevelTestAttempt(Base):

    __tablename__ = "level_test_attempts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False,
        index=True
    )

    source_level_id = Column(
        Integer,
        ForeignKey("levels.id"),
        nullable=False,
        index=True
    )

    target_level_id = Column(
        Integer,
        ForeignKey("levels.id"),
        nullable=False,
        index=True
    )

    score = Column(
        Integer,
        default=0,
        nullable=False
    )

    total_questions = Column(
        Integer,
        default=10,
        nullable=False
    )

    required_score = Column(
        Integer,
        default=8,
        nullable=False
    )

    passed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    started_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    submitted_at = Column(
        DateTime,
        nullable=True
    )


# ============================================================
# 4. INDIVIDUAL ANSWERS
# ============================================================

class LevelTestAnswer(Base):

    __tablename__ = "level_test_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    attempt_id = Column(
        Integer,
        ForeignKey("level_test_attempts.id"),
        nullable=False,
        index=True
    )

    question_id = Column(
        Integer,
        ForeignKey("level_test_questions.id"),
        nullable=False,
        index=True
    )

    selected_answer = Column(
        Text,
        nullable=True
    )

    correct_answer = Column(
        Text,
        nullable=False
    )

    is_correct = Column(
        Boolean,
        default=False,
        nullable=False
    )

    # Snapshot is deliberately stored here.
    # Even if faculty changes the question later,
    # old attempt feedback remains understandable.
    concept_gap = Column(
        String(255),
        nullable=True
    )

    explanation = Column(
        Text,
        nullable=True
    )

    answered_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (

        UniqueConstraint(
            "attempt_id",
            "question_id",
            name="uq_attempt_question_answer"
        ),

    )