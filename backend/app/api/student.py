from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.course import Course
from app.models.year import AcademicYear
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic


router = APIRouter(
    prefix="/student",
    tags=["Student"]
)


# =========================================================
# GET ALL COURSES
# =========================================================

@router.get("/courses")
def get_courses(
    db: Session = Depends(get_db)
):

    courses = (
        db.query(Course)
        .order_by(Course.name)
        .all()
    )

    return {
        "courses": [
            {
                "id": course.id,
                "name": course.name,
                "code": course.code
            }
            for course in courses
        ]
    }


# =========================================================
# GET YEARS FOR SELECTED COURSE
# =========================================================

@router.get("/courses/{course_id}/years")
def get_course_years(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )


    years = (
        db.query(AcademicYear)
        .filter(
            AcademicYear.course_id == course_id
        )
        .order_by(
            AcademicYear.year_number
        )
        .all()
    )


    return {

        "course": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        },

        "years": [
            {
                "id": year.id,
                "name": year.name,
                "year_number":
                    year.year_number
            }
            for year in years
        ]
    }


# =========================================================
# GET SUBJECTS
# =========================================================

@router.get(
    "/courses/{course_id}/years/{year_id}/subjects"
)
def get_subjects(
    course_id: int,
    year_id: int,
    db: Session = Depends(get_db)
):

    subjects = (
        db.query(Subject)
        .filter(
            Subject.course_id == course_id,
            Subject.year_id == year_id
        )
        .order_by(Subject.name)
        .all()
    )


    return {

        "subjects": [
            {
                "id": subject.id,
                "name": subject.name,
                "code": subject.code
            }
            for subject in subjects
        ]

    }


# =========================================================
# GET SUBJECT LEARNING PATH
# =========================================================

@router.get(
    "/subjects/{subject_id}/learning-path"
)
def get_subject_learning_path(
    subject_id: int,
    db: Session = Depends(get_db)
):

    subject = (
        db.query(Subject)
        .filter(
            Subject.id == subject_id
        )
        .first()
    )


    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )


    course = (
        db.query(Course)
        .filter(
            Course.id == subject.course_id
        )
        .first()
    )


    academic_year = (
        db.query(AcademicYear)
        .filter(
            AcademicYear.id == subject.year_id
        )
        .first()
    )


    levels = (
        db.query(Level)
        .filter(
            Level.subject_id == subject.id
        )
        .order_by(
            Level.level_order
        )
        .all()
    )


    level_list = []


    for level in levels:

        topics = (
            db.query(Topic)
            .filter(
                Topic.subject_id == subject.id,
                Topic.level_id == level.id
            )
            .order_by(
                Topic.topic_order
            )
            .all()
        )


        level_list.append(
            {
                "id": level.id,

                "name": level.name,

                "level_order":
                    level.level_order,

                "is_unlocked":
                    level.is_default_unlocked,

                "unlock_score_required":
                    level.unlock_score_required,

                "topics": [

                    {
                        "id": topic.id,

                        "title":
                            topic.title,

                        "description":
                            topic.description,

                        "topic_order":
                            topic.topic_order,

                        "visualization":
                            topic.visualization_type,

                        "game":
                            topic.game_type
                    }

                    for topic in topics
                ]
            }
        )


    return {

        "student_learning_path": {

            "course": {
                "id": course.id,
                "name": course.name,
                "code": course.code
            },

            "year": {
                "id": academic_year.id,
                "name": academic_year.name,
                "year_number":
                    academic_year.year_number
            },

            "subject": {
                "id": subject.id,
                "name": subject.name,
                "code": subject.code
            },

            "levels": level_list
        }
    }


# =========================================================
# OLD DEMO ENDPOINT
# KEEP FOR TESTING
# =========================================================

@router.get("/learning-path")
def get_demo_learning_path(
    db: Session = Depends(get_db)
):

    subject = (
        db.query(Subject)
        .filter(
            Subject.code == "PHY101"
        )
        .first()
    )


    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Physics subject not found"
        )


    return get_subject_learning_path(
        subject.id,
        db
    )