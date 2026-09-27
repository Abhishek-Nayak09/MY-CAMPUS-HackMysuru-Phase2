from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.portal_session import portal_user

from app.models.user import User
from app.models.topic import Topic
from app.models.subject import Subject
from app.models.doubt_ticket import DoubtTicket


router = APIRouter(
    prefix="/hod-analytics",
    tags=["HOD Analytics"],
)


# ============================================================
# ACCESS CONTROL
# ============================================================

def require_hod(
    user: User,
):

    if (
        user.role != "faculty"
        or
        str(
            user.faculty_role
            or ""
        )
        .strip()
        .lower()
        != "hod"
    ):

        raise HTTPException(
            status_code=403,
            detail="HOD access required",
        )


# ============================================================
# TIME HELPER
# ============================================================

def resolution_minutes(
    ticket: DoubtTicket,
):

    if not ticket.resolved_at:

        return None


    start_time = (
        ticket.started_at
        or
        ticket.created_at
    )


    if not start_time:

        return None


    seconds = (
        ticket.resolved_at
        - start_time
    ).total_seconds()


    return round(
        max(
            0.0,
            seconds / 60.0,
        ),
        1,
    )


# ============================================================
# HOD OVERVIEW
# ============================================================

@router.get(
    "/overview"
)
def hod_overview(

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    require_hod(
        user
    )


    # --------------------------------------------------------
    # PROFESSORS ONLY
    # HOD IS NOT INCLUDED AS A SUPPORT FACULTY MEMBER
    # --------------------------------------------------------

    faculty_users = (

        db.query(
            User
        )
        .filter(
            User.role == "faculty"
        )
        .order_by(
            User.full_name.asc()
        )
        .all()
    )


    professors = [

        faculty

        for faculty
        in faculty_users

        if (
            str(
                faculty.faculty_role
                or "professor"
            )
            .strip()
            .lower()
            != "hod"
        )
    ]


    faculty_rows = []

    department_times = []

    total_received = 0

    total_resolved = 0


    # --------------------------------------------------------
    # FACULTY-WISE ANALYTICS
    # --------------------------------------------------------

    for professor in professors:

        assigned_tickets = (

            db.query(
                DoubtTicket
            )
            .filter(
                DoubtTicket.assigned_faculty_id
                == professor.id
            )
            .order_by(
                DoubtTicket.created_at.desc()
            )
            .all()
        )


        received_count = len(
            assigned_tickets
        )


        resolved_tickets = [

            ticket

            for ticket
            in assigned_tickets

            if (
                ticket.status
                == "resolved"
            )
        ]


        resolved_count = len(
            resolved_tickets
        )


        pending_count = max(
            0,
            received_count
            - resolved_count,
        )


        total_received += (
            received_count
        )


        total_resolved += (
            resolved_count
        )


        faculty_times = []

        solved_questions = []


        # ----------------------------------------------------
        # SOLVED QUESTION HISTORY
        # ----------------------------------------------------

        for ticket in resolved_tickets:

            minutes = (
                resolution_minutes(
                    ticket
                )
            )


            if minutes is not None:

                faculty_times.append(
                    minutes
                )


                department_times.append(
                    minutes
                )


            subject = db.get(
                Subject,
                ticket.subject_id,
            )


            topic = db.get(
                Topic,
                ticket.topic_id,
            )


            solved_questions.append({

                "ticket_id":
                    ticket.id,

                "subject":
                    (
                        subject.name
                        if subject
                        else "Unknown Subject"
                    ),

                "topic":
                    (
                        topic.title
                        if topic
                        else "Unknown Topic"
                    ),

                "question":
                    ticket.doubt_text,

                "resolution_minutes":
                    minutes,

                "resolved_at":
                    ticket.resolved_at,

            })


        # ----------------------------------------------------
        # FACULTY AVERAGE RESOLUTION TIME
        # ----------------------------------------------------

        average_time = (

            round(
                sum(
                    faculty_times
                )
                /
                len(
                    faculty_times
                ),
                1,
            )

            if faculty_times

            else None
        )


        faculty_rows.append({

            "faculty_id":
                professor.id,

            "faculty_name":
                professor.full_name,

            "faculty_login_id":
                professor.login_id,

            "questions_received":
                received_count,

            "questions_resolved":
                resolved_count,

            "questions_pending":
                pending_count,

            "average_resolution_minutes":
                average_time,

            "solved_questions":
                solved_questions,

        })


    # --------------------------------------------------------
    # DEPARTMENT SUMMARY
    # --------------------------------------------------------

    department_average = (

        round(
            sum(
                department_times
            )
            /
            len(
                department_times
            ),
            1,
        )

        if department_times

        else None
    )


    return {

        "summary": {

            "active_professors":
                len(
                    professors
                ),

            "total_questions_received":
                total_received,

            "total_questions_resolved":
                total_resolved,

            "total_questions_pending":
                max(
                    0,
                    total_received
                    - total_resolved,
                ),

            "average_resolution_minutes":
                department_average,

        },


        # Data used for HOD table
        "faculty":
            faculty_rows,


        # Same compact data can directly feed
        # the frontend bar graph.
        "resolution_plot": [

            {

                "faculty_name":
                    row[
                        "faculty_name"
                    ],

                "average_resolution_minutes":
                    row[
                        "average_resolution_minutes"
                    ],

                "resolved":
                    row[
                        "questions_resolved"
                    ],

            }

            for row
            in faculty_rows

        ],

    }