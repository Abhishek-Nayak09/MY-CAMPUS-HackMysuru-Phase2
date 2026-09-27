from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic
from app.models.doubt_ticket import DoubtTicket


router = APIRouter(
    prefix="/tickets",
    tags=["Doubt Tickets"]
)


# =========================================================
# REQUEST MODELS
# =========================================================


class CreateTicketRequest(BaseModel):

    student_id: int

    subject_id: int

    level_id: int

    topic_id: int

    doubt_text: str

    weak_concept: str | None = None

    attempted_methods: str | None = None

    ai_attempted: bool = True


class ResolveTicketRequest(BaseModel):

    faculty_id: int

    faculty_response: str


# =========================================================
# HELPER
# =========================================================


def ticket_response(
    ticket: DoubtTicket,
    db: Session
):

    student = (
        db.query(User)
        .filter(
            User.id == ticket.student_id
        )
        .first()
    )


    subject = (
        db.query(Subject)
        .filter(
            Subject.id == ticket.subject_id
        )
        .first()
    )


    level = (
        db.query(Level)
        .filter(
            Level.id == ticket.level_id
        )
        .first()
    )


    topic = (
        db.query(Topic)
        .filter(
            Topic.id == ticket.topic_id
        )
        .first()
    )


    faculty = None


    if ticket.assigned_faculty_id:

        faculty = (
            db.query(User)
            .filter(
                User.id ==
                ticket.assigned_faculty_id
            )
            .first()
        )


    return {

        "id":
            ticket.id,

        "student": {

            "id":
                student.id
                if student
                else None,

            "name":
                student.full_name
                if student
                else "Unknown Student",

            "login_id":
                student.login_id
                if student
                else None

        },

        "subject": {

            "id":
                subject.id
                if subject
                else None,

            "name":
                subject.name
                if subject
                else "Unknown Subject"

        },

        "level": {

            "id":
                level.id
                if level
                else None,

            "name":
                level.name
                if level
                else "Unknown Level"

        },

        "topic": {

            "id":
                topic.id
                if topic
                else None,

            "title":
                topic.title
                if topic
                else "Unknown Topic"

        },

        "doubt_text":
            ticket.doubt_text,

        "weak_concept":
            ticket.weak_concept,

        "attempted_methods":
            ticket.attempted_methods,

        "ai_attempted":
            ticket.ai_attempted,

        "status":
            ticket.status,

        "assigned_faculty": {

            "id":
                faculty.id
                if faculty
                else None,

            "name":
                faculty.full_name
                if faculty
                else None

        },

        "faculty_response":
            ticket.faculty_response,

        "created_at":
            ticket.created_at,

        "started_at":
            ticket.started_at,

        "resolved_at":
            ticket.resolved_at

    }


# =========================================================
# STUDENT CREATE TICKET
# =========================================================


@router.post("")
def create_ticket(
    payload: CreateTicketRequest,
    db: Session = Depends(get_db)
):

    student = (
        db.query(User)
        .filter(
            User.id == payload.student_id,
            User.role == "student"
        )
        .first()
    )


    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )


    subject = (
        db.query(Subject)
        .filter(
            Subject.id ==
            payload.subject_id
        )
        .first()
    )


    if not subject:

        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )


    level = (
        db.query(Level)
        .filter(
            Level.id ==
            payload.level_id
        )
        .first()
    )


    if not level:

        raise HTTPException(
            status_code=404,
            detail="Level not found"
        )


    topic = (
        db.query(Topic)
        .filter(
            Topic.id ==
            payload.topic_id
        )
        .first()
    )


    if not topic:

        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )


    ticket = DoubtTicket(

        student_id=
            payload.student_id,

        subject_id=
            payload.subject_id,

        level_id=
            payload.level_id,

        topic_id=
            payload.topic_id,

        doubt_text=
            payload.doubt_text,

        weak_concept=
            payload.weak_concept,

        attempted_methods=
            payload.attempted_methods,

        ai_attempted=
            payload.ai_attempted,

        status="new"
    )


    db.add(ticket)

    db.commit()

    db.refresh(ticket)


    return {

        "status":
            "success",

        "message":
            "Doubt ticket created successfully",

        "ticket":
            ticket_response(
                ticket,
                db
            )

    }


# =========================================================
# PROFESSOR VIEW AVAILABLE + ASSIGNED TICKETS
# =========================================================


@router.get("/faculty/{faculty_id}")
def get_faculty_tickets(
    faculty_id: int,
    db: Session = Depends(get_db)
):

    faculty = (
        db.query(User)
        .filter(
            User.id == faculty_id,
            User.role == "faculty"
        )
        .first()
    )


    if not faculty:

        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )


    tickets = (
        db.query(DoubtTicket)
        .filter(
            or_(
                DoubtTicket.assigned_faculty_id
                == faculty_id,

                DoubtTicket.assigned_faculty_id
                .is_(None)
            )
        )
        .order_by(
            DoubtTicket.created_at.desc()
        )
        .all()
    )


    return {

        "faculty": {

            "id":
                faculty.id,

            "name":
                faculty.full_name

        },

        "tickets": [

            ticket_response(
                ticket,
                db
            )

            for ticket in tickets
        ]

    }


# =========================================================
# PROFESSOR TAKE / START TICKET
# =========================================================


@router.patch("/{ticket_id}/start")
def start_ticket(
    ticket_id: int,
    faculty_id: int,
    db: Session = Depends(get_db)
):

    faculty = (
        db.query(User)
        .filter(
            User.id == faculty_id,
            User.role == "faculty"
        )
        .first()
    )


    if not faculty:

        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )


    ticket = (
        db.query(DoubtTicket)
        .filter(
            DoubtTicket.id == ticket_id
        )
        .first()
    )


    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )


    if (
        ticket.assigned_faculty_id
        is not None
        and
        ticket.assigned_faculty_id
        != faculty_id
    ):

        raise HTTPException(
            status_code=409,
            detail="Ticket already assigned to another faculty member"
        )


    if ticket.status == "resolved":

        raise HTTPException(
            status_code=400,
            detail="Resolved ticket cannot be restarted"
        )


    ticket.assigned_faculty_id = (
        faculty_id
    )


    ticket.status = (
        "in_progress"
    )


    if ticket.started_at is None:

        ticket.started_at = (
            datetime.utcnow()
        )


    db.commit()

    db.refresh(ticket)


    return {

        "status":
            "success",

        "message":
            "Ticket moved to In Progress",

        "ticket":
            ticket_response(
                ticket,
                db
            )

    }


# =========================================================
# PROFESSOR RESOLVE TICKET
# =========================================================


@router.patch("/{ticket_id}/resolve")
def resolve_ticket(
    ticket_id: int,
    payload: ResolveTicketRequest,
    db: Session = Depends(get_db)
):

    faculty = (
        db.query(User)
        .filter(
            User.id ==
            payload.faculty_id,

            User.role ==
            "faculty"
        )
        .first()
    )


    if not faculty:

        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )


    ticket = (
        db.query(DoubtTicket)
        .filter(
            DoubtTicket.id ==
            ticket_id
        )
        .first()
    )


    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )


    if (
        ticket.assigned_faculty_id
        is not None
        and
        ticket.assigned_faculty_id
        != payload.faculty_id
    ):

        raise HTTPException(
            status_code=409,
            detail="Ticket belongs to another faculty member"
        )


    ticket.assigned_faculty_id = (
        payload.faculty_id
    )


    if ticket.started_at is None:

        ticket.started_at = (
            datetime.utcnow()
        )


    ticket.faculty_response = (
        payload.faculty_response
    )


    ticket.status = (
        "resolved"
    )


    ticket.resolved_at = (
        datetime.utcnow()
    )


    db.commit()

    db.refresh(ticket)


    return {

        "status":
            "success",

        "message":
            "Ticket resolved successfully",

        "ticket":
            ticket_response(
                ticket,
                db
            )

    }


# =========================================================
# STUDENT VIEW OWN TICKETS
# =========================================================


@router.get("/student/{student_id}")
def get_student_tickets(
    student_id: int,
    db: Session = Depends(get_db)
):

    tickets = (
        db.query(DoubtTicket)
        .filter(
            DoubtTicket.student_id ==
            student_id
        )
        .order_by(
            DoubtTicket.created_at.desc()
        )
        .all()
    )


    return {

        "tickets": [

            ticket_response(
                ticket,
                db
            )

            for ticket in tickets
        ]

    }