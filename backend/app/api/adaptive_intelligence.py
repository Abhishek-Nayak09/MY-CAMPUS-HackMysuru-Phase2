from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.adaptive_engine import (
    build_adaptive_snapshot,
)

from app.db.database import get_db

from app.models.topic import Topic
from app.models.user import User


router = APIRouter(
    prefix="/adaptive-intelligence",
    tags=["Adaptive Intelligence"],
)


# ============================================================
# HELPERS
# ============================================================

def get_student_or_404(
    db: Session,
    student_id: int,
):

    student = (
        db.query(User)
        .filter(
            User.id == student_id
        )
        .first()
    )


    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found.",
        )


    if student.role != "student":

        raise HTTPException(
            status_code=400,
            detail="User is not a student.",
        )


    return student


def get_topic_or_404(
    db: Session,
    topic_id: int,
):

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )


    if topic is None:

        raise HTTPException(
            status_code=404,
            detail="Topic not found.",
        )


    return topic


# ============================================================
# 1. FULL STUDENT ADAPTIVE PROFILE
# ============================================================

@router.get(
    "/profile/{student_id}"
)
def adaptive_profile(
    student_id: int,
    db: Session = Depends(get_db),
):

    student = get_student_or_404(
        db,
        student_id,
    )


    snapshot = build_adaptive_snapshot(
        db=db,
        student_id=student_id,
        topic_id=None,
    )


    return {

        "status":
            "success",

        "student":
            {

                "id":
                    student.id,

                "name":
                    student.full_name,
            },

        "adaptive_profile":
            snapshot,
    }


# ============================================================
# 2. TOPIC-SPECIFIC ADAPTIVE DECISION
# ============================================================

@router.get(
    "/topic/{student_id}/{topic_id}"
)
def adaptive_topic_decision(
    student_id: int,
    topic_id: int,
    db: Session = Depends(get_db),
):

    student = get_student_or_404(
        db,
        student_id,
    )


    topic = get_topic_or_404(
        db,
        topic_id,
    )


    snapshot = build_adaptive_snapshot(
        db=db,
        student_id=student_id,
        topic_id=topic_id,
    )


    return {

        "status":
            "success",

        "student":
            {

                "id":
                    student.id,

                "name":
                    student.full_name,
            },

        "topic":
            {

                "id":
                    topic.id,

                "title":
                    topic.title,
            },

        "decision":
            snapshot,
    }