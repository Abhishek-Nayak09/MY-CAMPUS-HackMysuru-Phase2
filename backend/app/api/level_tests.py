import json

from datetime import datetime
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic

from app.models.level_test import (
    StudentLevelProgress,
    LevelTestQuestion,
    LevelTestAttempt,
    LevelTestAnswer
)


router = APIRouter(
    prefix="/level-tests",
    tags=["Level Unlock Tests"]
)


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class AnswerItem(BaseModel):

    question_id: int
    selected_answer: str


class SubmitTestRequest(BaseModel):

    user_id: int
    answers: List[AnswerItem]


# ============================================================
# HELPERS
# ============================================================

def now_utc():

    return datetime.utcnow()


def get_user_or_404(
    db: Session,
    user_id: int
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    return user


def get_level_or_404(
    db: Session,
    level_id: int
):

    level = (
        db.query(Level)
        .filter(
            Level.id == level_id
        )
        .first()
    )

    if not level:

        raise HTTPException(
            status_code=404,
            detail="Level not found."
        )

    return level


def get_or_create_progress(
    db: Session,
    user_id: int,
    subject_id: int,
    level: Level
):

    progress = (
        db.query(StudentLevelProgress)
        .filter(
            StudentLevelProgress.user_id == user_id,
            StudentLevelProgress.subject_id == subject_id,
            StudentLevelProgress.level_id == level.id
        )
        .first()
    )


    if progress:

        return progress


    default_unlocked = bool(
        getattr(
            level,
            "is_default_unlocked",
            False
        )
    )


    progress = StudentLevelProgress(

        user_id=
            user_id,

        subject_id=
            subject_id,

        level_id=
            level.id,

        is_unlocked=
            default_unlocked,

        best_score=
            0,

        unlocked_at=
            now_utc()
            if default_unlocked
            else None
    )


    db.add(progress)

    db.flush()

    return progress


def load_options(
    options_json: str
):

    try:

        options = json.loads(
            options_json
        )

        if not isinstance(
            options,
            list
        ):

            return []


        return options


    except Exception:

        return []


def get_test_questions(
    db: Session,
    source_level_id: int
):

    questions = (
        db.query(LevelTestQuestion)
        .filter(
            LevelTestQuestion.source_level_id
            == source_level_id,

            LevelTestQuestion.is_active
            == True
        )
        .order_by(
            LevelTestQuestion.question_order
        )
        .all()
    )


    if not questions:

        raise HTTPException(
            status_code=404,
            detail=(
                "No unlock test exists "
                "for this level."
            )
        )


    return questions


# ============================================================
# 1. STUDENT LEVEL STATUS
# ============================================================

@router.get(
    "/status/{user_id}/{subject_id}"
)
def get_level_status(
    user_id: int,
    subject_id: int,
    db: Session = Depends(get_db)
):

    get_user_or_404(
        db,
        user_id
    )


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
            detail="Subject not found."
        )


    levels = (
        db.query(Level)
        .filter(
            Level.subject_id == subject_id
        )
        .order_by(
            Level.level_order
        )
        .all()
    )


    if not levels:

        raise HTTPException(
            status_code=404,
            detail=(
                "No learning levels found "
                "for this subject."
            )
        )


    output = []


    for level in levels:

        progress = (
            get_or_create_progress(
                db=db,
                user_id=user_id,
                subject_id=subject_id,
                level=level
            )
        )


        unlock_score_required = (
            getattr(
                level,
                "unlock_score_required",
                0
            )
            or 0
        )


        output.append({

            "level_id":
                level.id,

            "level_name":
                level.name,

            "level_order":
                level.level_order,

            "is_unlocked":
                progress.is_unlocked,

            "best_score":
                progress.best_score,

            "unlock_score_required":
                unlock_score_required,

            "unlocked_at":
                progress.unlocked_at,

            "last_attempt_at":
                progress.last_attempt_at
        })


    db.commit()


    return {

        "student_id":
            user_id,

        "subject": {

            "id":
                subject.id,

            "name":
                subject.name
        },

        "levels":
            output
    }


# ============================================================
# 2. GET TEST FOR A SOURCE LEVEL
#
# Example:
# source = Entry
# target = Basics
# ============================================================

@router.get(
    "/test/{user_id}/{source_level_id}"
)
def get_unlock_test(
    user_id: int,
    source_level_id: int,
    db: Session = Depends(get_db)
):

    get_user_or_404(
        db,
        user_id
    )


    source_level = (
        get_level_or_404(
            db,
            source_level_id
        )
    )


    source_progress = (
        get_or_create_progress(
            db=db,
            user_id=user_id,
            subject_id=source_level.subject_id,
            level=source_level
        )
    )


    db.commit()


    if not source_progress.is_unlocked:

        raise HTTPException(
            status_code=403,
            detail=(
                f"{source_level.name} level "
                "is currently locked."
            )
        )


    questions = (
        get_test_questions(
            db,
            source_level_id
        )
    )


    # All questions in one unlock test
    # must point to the same target level.

    target_level_id = (
        questions[0].target_level_id
    )


    subject_id = (
        questions[0].subject_id
    )


    for question in questions:

        if (
            question.target_level_id
            != target_level_id
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "Invalid question bank: "
                    "multiple target levels found."
                )
            )


        if (
            question.subject_id
            != subject_id
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "Invalid question bank: "
                    "multiple subjects found."
                )
            )


    target_level = (
        get_level_or_404(
            db,
            target_level_id
        )
    )


    required_score = (
        getattr(
            target_level,
            "unlock_score_required",
            8
        )
        or 8
    )


    # --------------------------------------------------------
    # IMPORTANT:
    # Correct answers are NEVER returned here.
    # Student only receives question + options.
    # --------------------------------------------------------

    question_output = []


    for question in questions:

        topic = (
            db.query(Topic)
            .filter(
                Topic.id == question.topic_id
            )
            .first()
        )


        question_output.append({

            "id":
                question.id,

            "order":
                question.question_order,

            "topic_id":
                question.topic_id,

            "topic_title":
                topic.title
                if topic
                else None,

            "question":
                question.question_text,

            "options":
                load_options(
                    question.options_json
                )
        })


    return {

        "student_id":
            user_id,

        "subject_id":
            subject_id,

        "source_level": {

            "id":
                source_level.id,

            "name":
                source_level.name
        },

        "target_level": {

            "id":
                target_level.id,

            "name":
                target_level.name
        },

        "total_questions":
            len(question_output),

        "required_score":
            required_score,

        "pass_rule":
            f"{required_score}/{len(question_output)}",

        "questions":
            question_output
    }


# ============================================================
# 3. SUBMIT TEST
# ============================================================

@router.post(
    "/submit/{source_level_id}"
)
def submit_unlock_test(
    source_level_id: int,
    payload: SubmitTestRequest,
    db: Session = Depends(get_db)
):

    student = (
        get_user_or_404(
            db,
            payload.user_id
        )
    )


    source_level = (
        get_level_or_404(
            db,
            source_level_id
        )
    )


    questions = (
        get_test_questions(
            db,
            source_level_id
        )
    )


    if len(questions) != 10:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unlock test must contain "
                "exactly 10 active questions."
            )
        )


    subject_id = (
        questions[0].subject_id
    )


    target_level_id = (
        questions[0].target_level_id
    )


    # --------------------------------------------------------
    # VALIDATE QUESTION BANK
    # --------------------------------------------------------

    for question in questions:

        if (
            question.subject_id
            != subject_id
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "Question bank contains "
                    "mixed subjects."
                )
            )


        if (
            question.target_level_id
            != target_level_id
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "Question bank contains "
                    "mixed target levels."
                )
            )


    target_level = (
        get_level_or_404(
            db,
            target_level_id
        )
    )


    # --------------------------------------------------------
    # CHECK SOURCE LEVEL ACCESS
    # --------------------------------------------------------

    source_progress = (
        get_or_create_progress(
            db=db,
            user_id=student.id,
            subject_id=subject_id,
            level=source_level
        )
    )


    if not source_progress.is_unlocked:

        db.rollback()

        raise HTTPException(
            status_code=403,
            detail=(
                f"{source_level.name} level "
                "is locked."
            )
        )


    # --------------------------------------------------------
    # VALIDATE ANSWERS
    # --------------------------------------------------------

    if len(payload.answers) != 10:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=(
                "Exactly 10 answers "
                "must be submitted."
            )
        )


    submitted_answers = {}


    for answer in payload.answers:

        if answer.question_id in submitted_answers:

            db.rollback()

            raise HTTPException(
                status_code=400,
                detail=(
                    "Duplicate question answer "
                    "was submitted."
                )
            )


        submitted_answers[
            answer.question_id
        ] = answer.selected_answer


    expected_question_ids = {
        question.id
        for question in questions
    }


    submitted_question_ids = set(
        submitted_answers.keys()
    )


    if (
        expected_question_ids
        != submitted_question_ids
    ):

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=(
                "Submitted answers do not match "
                "the current 10-question test."
            )
        )


    # --------------------------------------------------------
    # PASS RULE
    # --------------------------------------------------------

    required_score = (
        getattr(
            target_level,
            "unlock_score_required",
            8
        )
        or 8
    )


    # --------------------------------------------------------
    # CREATE ATTEMPT
    # --------------------------------------------------------

    attempt = LevelTestAttempt(

        user_id=
            student.id,

        subject_id=
            subject_id,

        source_level_id=
            source_level.id,

        target_level_id=
            target_level.id,

        score=
            0,

        total_questions=
            len(questions),

        required_score=
            required_score,

        passed=
            False,

        submitted_at=
            None
    )


    db.add(attempt)

    db.flush()


    # --------------------------------------------------------
    # MARK ANSWERS
    # --------------------------------------------------------

    score = 0

    wrong_answers = []


    for question in questions:

        selected_answer = (
            submitted_answers[
                question.id
            ].strip()
        )


        correct_answer = (
            question.correct_answer.strip()
        )


        is_correct = (
            selected_answer
            == correct_answer
        )


        if is_correct:

            score += 1


        answer_record = LevelTestAnswer(

            attempt_id=
                attempt.id,

            question_id=
                question.id,

            selected_answer=
                selected_answer,

            correct_answer=
                correct_answer,

            is_correct=
                is_correct,

            concept_gap=
                None
                if is_correct
                else question.concept_gap,

            explanation=
                None
                if is_correct
                else question.explanation
        )


        db.add(
            answer_record
        )


        # ----------------------------------------------------
        # WRONG ANSWER FEEDBACK
        # ----------------------------------------------------

        if not is_correct:

            topic = (
                db.query(Topic)
                .filter(
                    Topic.id
                    == question.topic_id
                )
                .first()
            )


            wrong_answers.append({

                "question_id":
                    question.id,

                "question":
                    question.question_text,

                "selected_answer":
                    selected_answer,

                "correct_answer":
                    correct_answer,

                "concept_gap":
                    question.concept_gap,

                "explanation":
                    question.explanation,

                "topic": {

                    "id":
                        question.topic_id,

                    "title":
                        topic.title
                        if topic
                        else None
                }
            })


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    passed = (
        score >= required_score
    )


    attempt.score = (
        score
    )

    attempt.passed = (
        passed
    )

    attempt.submitted_at = (
        now_utc()
    )


    # --------------------------------------------------------
    # UPDATE SOURCE PROGRESS
    # --------------------------------------------------------

    if score > source_progress.best_score:

        source_progress.best_score = (
            score
        )


    source_progress.last_attempt_at = (
        now_utc()
    )


    # --------------------------------------------------------
    # TARGET LEVEL PROGRESS
    # --------------------------------------------------------

    target_progress = (
        get_or_create_progress(
            db=db,
            user_id=student.id,
            subject_id=subject_id,
            level=target_level
        )
    )


    newly_unlocked = False


    if passed:

        if not target_progress.is_unlocked:

            target_progress.is_unlocked = (
                True
            )

            target_progress.unlocked_at = (
                now_utc()
            )

            newly_unlocked = True


    db.commit()

    db.refresh(attempt)


    # --------------------------------------------------------
    # RESULT MESSAGE
    # --------------------------------------------------------

    if passed:

        result_message = (
            f"Congratulations! "
            f"You scored {score}/10 and "
            f"unlocked {target_level.name}."
        )

    else:

        result_message = (
            f"You scored {score}/10. "
            f"You need {required_score}/10 "
            f"to unlock {target_level.name}. "
            f"Review the identified concept gaps "
            f"and try again."
        )


    return {

        "attempt_id":
            attempt.id,

        "student_id":
            student.id,

        "subject_id":
            subject_id,

        "source_level": {

            "id":
                source_level.id,

            "name":
                source_level.name
        },

        "target_level": {

            "id":
                target_level.id,

            "name":
                target_level.name
        },

        "score":
            score,

        "total_questions":
            len(questions),

        "required_score":
            required_score,

        "passed":
            passed,

        "newly_unlocked":
            newly_unlocked,

        "target_level_unlocked":
            target_progress.is_unlocked,

        "wrong_count":
            len(wrong_answers),

        "concept_gaps": [
            {

                "topic_id":
                    item["topic"]["id"],

                "topic_title":
                    item["topic"]["title"],

                "concept":
                    item["concept_gap"]
            }
            for item in wrong_answers
        ],

        "wrong_answers":
            wrong_answers,

        "message":
            result_message
    }


# ============================================================
# 4. ATTEMPT HISTORY
# ============================================================

@router.get(
    "/history/{user_id}/{subject_id}"
)
def get_test_history(
    user_id: int,
    subject_id: int,
    db: Session = Depends(get_db)
):

    get_user_or_404(
        db,
        user_id
    )


    attempts = (
        db.query(LevelTestAttempt)
        .filter(
            LevelTestAttempt.user_id
            == user_id,

            LevelTestAttempt.subject_id
            == subject_id
        )
        .order_by(
            LevelTestAttempt.id.desc()
        )
        .all()
    )


    output = []


    for attempt in attempts:

        source_level = (
            db.query(Level)
            .filter(
                Level.id
                == attempt.source_level_id
            )
            .first()
        )


        target_level = (
            db.query(Level)
            .filter(
                Level.id
                == attempt.target_level_id
            )
            .first()
        )


        output.append({

            "attempt_id":
                attempt.id,

            "source_level":
                source_level.name
                if source_level
                else None,

            "target_level":
                target_level.name
                if target_level
                else None,

            "score":
                attempt.score,

            "total_questions":
                attempt.total_questions,

            "required_score":
                attempt.required_score,

            "passed":
                attempt.passed,

            "submitted_at":
                attempt.submitted_at
        })


    return {

        "student_id":
            user_id,

        "subject_id":
            subject_id,

        "total_attempts":
            len(output),

        "attempts":
            output
    }