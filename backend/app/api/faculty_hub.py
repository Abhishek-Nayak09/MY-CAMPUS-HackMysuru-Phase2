"""Topic resources and student/faculty doubt exchange.

This module handles:
- Faculty learning resources
- Student -> Faculty doubt tickets
- AI-generated faculty handoff summaries
"""

from pathlib import Path
from uuid import uuid4
from urllib.parse import urlparse

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)

from fastapi.responses import FileResponse

from pydantic import BaseModel, Field

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.portal_session import portal_user

from app.models.user import User
from app.models.topic import Topic
from app.models.subject import Subject
from app.models.level import Level
from app.models.level_test import StudentLevelProgress
from app.models.learning_content import LearningContent

from app.api import tickets

# Reuse the already working AI Tutor engine.
from app.api.ai_tutor import (
    call_openai,
    get_topic_context,
    clean_text,
    limit_text,
    OPENAI_MODEL,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/faculty-hub",
    tags=["Faculty and Student Hub"],
)


# ============================================================
# RESOURCE CONFIG
# ============================================================

RESOURCE_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "resource_files"
)


MAX_BYTES = (
    25
    * 1024
    * 1024
)


EXTENSIONS = {
    ".pdf",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    ".mp4",
    ".webm",
    ".pptx",
    ".docx",
}


TYPES = {
    "notes",
    "video",
    "visualization",
    "game",
}


# ============================================================
# ACCESS HELPERS
# ============================================================

def faculty(
    user
):

    if user.role != "faculty":

        raise HTTPException(
            403,
            "Faculty access required",
        )


def topic_access(
    db,
    user,
    topic_id
):

    topic = db.get(
        Topic,
        topic_id,
    )


    if not topic:

        raise HTTPException(
            404,
            "Topic not found",
        )


    if user.role == "student":

        level = db.get(
            Level,
            topic.level_id,
        )


        progress = (
            db.query(
                StudentLevelProgress
            )
            .filter_by(
                user_id=user.id,
                level_id=topic.level_id,
                subject_id=topic.subject_id,
            )
            .first()
        )


        allowed = (
            progress.is_unlocked
            if progress
            else bool(
                level
                and
                level.is_default_unlocked
            )
        )


        if not allowed:

            raise HTTPException(
                403,
                (
                    "Complete the level unlock test "
                    "before accessing this topic."
                ),
            )


    elif user.role != "faculty":

        raise HTTPException(
            403,
            "Student or faculty access required",
        )


    return topic


# ============================================================
# RESOURCE JSON
# ============================================================

def resource_json(
    item,
    db
):

    owner = db.get(
        User,
        item.uploaded_by,
    )


    topic = db.get(
        Topic,
        item.topic_id,
    )


    return dict(

        id=item.id,

        title=item.title,

        description=item.description,

        topic_id=item.topic_id,

        topic_title=(
            topic.title
            if topic
            else ""
        ),

        resource_type=(
            item.resource_type
            .removeprefix(
                "faculty_"
            )
        ),

        faculty_name=(
            owner.full_name
            if owner
            else "Faculty"
        ),

        created_at=item.created_at,

        is_file=bool(
            item.resource_url
            and
            item.resource_url.startswith(
                "file:"
            )
        ),

        url=(
            None
            if (
                item.resource_url
                or ""
            ).startswith(
                "file:"
            )
            else item.resource_url
        ),
    )


# ============================================================
# FACULTY RESOURCE CATALOG
# ============================================================

@router.get(
    "/catalog"
)
def catalog(

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    faculty(
        user
    )


    return {

        "subjects": [

            dict(
                id=s.id,
                name=s.name,
            )

            for s
            in db.query(
                Subject
            ).order_by(
                Subject.id
            )

        ],

        "topics": [

            dict(
                id=t.id,
                title=t.title,
                subject_id=t.subject_id,
                level_id=t.level_id,
            )

            for t
            in db.query(
                Topic
            ).order_by(
                Topic.level_id,
                Topic.topic_order,
            )

        ],
    }


# ============================================================
# UPLOAD FACULTY RESOURCE
# ============================================================

@router.post(
    "/resources",
    status_code=201,
)
async def upload_resource(

    topic_id: int = Form(
        ...
    ),

    title: str = Form(
        ...,
        min_length=1,
        max_length=200,
    ),

    resource_type: str = Form(
        ...
    ),

    description: str = Form(
        "",
        max_length=5000,
    ),

    url: str = Form(
        "",
        max_length=2000,
    ),

    file: UploadFile | None = File(
        None
    ),

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    faculty(
        user
    )


    topic_access(
        db,
        user,
        topic_id,
    )


    title = title.strip()

    url = url.strip()


    if (
        not title
        or
        resource_type not in TYPES
    ):

        raise HTTPException(
            400,
            (
                "Choose a resource type "
                "and enter a title."
            ),
        )


    if (
        bool(
            file
            and
            file.filename
        )
        ==
        bool(
            url
        )
    ):

        raise HTTPException(
            400,
            (
                "Choose either one file "
                "or one HTTP(S) link."
            ),
        )


    stored = None


    if url:

        parsed = urlparse(
            url
        )


        if (
            parsed.scheme
            not in (
                "http",
                "https",
            )
            or
            not parsed.netloc
            or
            parsed.username
            or
            parsed.password
        ):

            raise HTTPException(
                400,
                (
                    "Use a valid HTTP(S) link "
                    "without embedded credentials."
                ),
            )


        resource_url = url


    else:

        suffix = (
            Path(
                file.filename
            )
            .suffix
            .lower()
        )


        if suffix not in EXTENSIONS:

            raise HTTPException(
                400,
                (
                    "Supported files: PDF, TXT, "
                    "PNG, JPG, MP4, WEBM, "
                    "PPTX, DOCX."
                ),
            )


        RESOURCE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )


        stored = (
            RESOURCE_DIR
            /
            (
                uuid4().hex
                + suffix
            )
        )


        total = 0


        try:

            with stored.open(
                "xb"
            ) as target:

                while chunk := (
                    await file.read(
                        1024
                        * 1024
                    )
                ):

                    total += len(
                        chunk
                    )


                    if total > MAX_BYTES:

                        raise HTTPException(
                            413,
                            (
                                "File must be "
                                "25 MB or smaller."
                            ),
                        )


                    target.write(
                        chunk
                    )


            if not total:

                raise HTTPException(
                    400,
                    (
                        "Empty files are "
                        "not supported."
                    ),
                )


        except Exception:

            stored.unlink(
                missing_ok=True
            )

            raise


        finally:

            await file.close()


        resource_url = (
            "file:"
            + stored.name
        )


    item = LearningContent(

        topic_id=topic_id,

        title=title,

        description=(
            description.strip()
        ),

        resource_type=(
            "faculty_"
            + resource_type
        ),

        resource_url=resource_url,

        uploaded_by=user.id,

        content_order=1000,

        is_active=True,
    )


    try:

        db.add(
            item
        )

        db.commit()

        db.refresh(
            item
        )


    except Exception:

        db.rollback()


        if stored:

            stored.unlink(
                missing_ok=True
            )


        raise


    return resource_json(
        item,
        db,
    )


# ============================================================
# FACULTY RESOURCE LIST
# ============================================================

@router.get(
    "/resources/mine"
)
def mine(

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    faculty(
        user
    )


    resources = (

        db.query(
            LearningContent
        )
        .filter(
            LearningContent.uploaded_by
            == user.id,

            LearningContent.is_active
            == True,
        )
        .order_by(
            LearningContent.created_at.desc()
        )
        .all()
    )


    return {

        "resources": [

            resource_json(
                r,
                db
            )

            for r
            in resources

        ]
    }


# ============================================================
# TOPIC RESOURCE LIST
# ============================================================

@router.get(
    "/resources/topic/{topic_id}"
)
def topic_resources(

    topic_id: int,

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    topic_access(
        db,
        user,
        topic_id,
    )


    resources = (

        db.query(
            LearningContent
        )
        .filter(

            LearningContent.topic_id
            == topic_id,

            LearningContent.uploaded_by
            .isnot(
                None
            ),

            LearningContent.is_active
            == True,
        )
        .order_by(
            LearningContent.created_at.desc()
        )
        .all()
    )


    return {

        "resources": [

            resource_json(
                r,
                db
            )

            for r
            in resources

        ]
    }


# ============================================================
# RESOURCE DOWNLOAD
# ============================================================

@router.get(
    "/resources/{resource_id}/download"
)
def download(

    resource_id: int,

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    item = db.get(
        LearningContent,
        resource_id,
    )


    if (
        not item
        or
        not item.is_active
        or
        not item.uploaded_by
        or
        not (
            item.resource_url
            or ""
        ).startswith(
            "file:"
        )
    ):

        raise HTTPException(
            404,
            "Resource file not found",
        )


    topic_access(
        db,
        user,
        item.topic_id,
    )


    name = (
        item.resource_url[
            5:
        ]
    )


    target = (
        RESOURCE_DIR
        /
        name
    ).resolve()


    if (
        target.parent
        !=
        RESOURCE_DIR.resolve()
        or
        not target.is_file()
    ):

        raise HTTPException(
            404,
            "Resource file not found",
        )


    return FileResponse(

        target,

        filename=(
            "resource-"
            + str(
                item.id
            )
            + target.suffix
        ),

        media_type=(
            "application/octet-stream"
        ),

        headers={
            "X-Content-Type-Options":
                "nosniff"
        },
    )


# ============================================================
# DOUBT SCHEMAS
# ============================================================

class Doubt(
    BaseModel
):

    topic_id: int

    doubt_text: str = Field(
        min_length=3,
        max_length=5000,
    )

    ai_attempted: bool = False


class Reply(
    BaseModel
):

    faculty_response: str = Field(
        min_length=3,
        max_length=5000,
    )


# ============================================================
# AI FACULTY HANDOFF SCHEMAS
# ============================================================

class FacultyHandoffHistoryMessage(
    BaseModel
):

    role: str

    content: str


class FacultyHandoffRequest(
    BaseModel
):

    topic_id: int

    history: list[
        FacultyHandoffHistoryMessage
    ] = Field(
        default_factory=list
    )


class FacultyHandoffResponse(
    BaseModel
):

    summary: str

    topic_id: int

    topic_title: str

    provider: str

    model: str | None = None

    ai_attempted: bool


# ============================================================
# FACULTY HANDOFF HELPERS
# ============================================================

def handoff_history_text(
    history: list[
        FacultyHandoffHistoryMessage
    ]
) -> str:

    blocks = []


    for index, item in enumerate(
        history[-12:],
        start=1,
    ):

        role = clean_text(
            item.role
        ).lower()


        if role not in {
            "user",
            "assistant",
        }:

            continue


        content = limit_text(
            item.content,
            1800,
        )


        if not content:

            continue


        speaker = (
            "STUDENT"
            if role == "user"
            else "AI TUTOR"
        )


        blocks.append(
            (
                f"{index}. "
                f"{speaker}: "
                f"{content}"
            )
        )


    if not blocks:

        return (
            "No AI Tutor conversation "
            "was recorded."
        )


    return "\n".join(
        blocks
    )


def build_local_handoff_summary(
    topic_title: str,
    history: list[
        FacultyHandoffHistoryMessage
    ],
) -> str:

    student_messages = []


    for item in history[-12:]:

        if (
            clean_text(
                item.role
            ).lower()
            == "user"
        ):

            content = limit_text(
                item.content,
                500,
            )


            if content:

                student_messages.append(
                    content
                )


    if student_messages:

        recent_doubt = (
            student_messages[-1]
        )


        return (
            f'Student is studying '
            f'"{topic_title}". '
            f'The latest difficulty expressed was: '
            f'"{recent_doubt}". '
            f'The student has already used the AI Tutor '
            f'for this topic. Please review the previous '
            f'learning attempt and explain the concept '
            f'using a different approach rather than '
            f'repeating the same explanation.'
        )


    return (
        f'Student is requesting faculty support for '
        f'"{topic_title}". '
        f'No detailed AI Tutor conversation was available '
        f'for automatic analysis. Please identify the exact '
        f'concept difficulty with the student and explain it '
        f'using a suitable alternative approach.'
    )


# ============================================================
# GENERATE AI FACULTY HANDOFF
# ============================================================

@router.post(
    "/doubts/handoff",
    response_model=(
        FacultyHandoffResponse
    ),
)
def generate_faculty_handoff(

    payload: FacultyHandoffRequest,

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    if user.role != "student":

        raise HTTPException(
            403,
            "Student access required",
        )


    topic = topic_access(
        db,
        user,
        payload.topic_id,
    )


    context = get_topic_context(
        db,
        payload.topic_id,
    )


    history_text = (
        handoff_history_text(
            payload.history
        )
    )


    has_ai_history = any(

        clean_text(
            item.role
        ).lower()
        in {
            "user",
            "assistant",
        }

        and
        bool(
            clean_text(
                item.content
            )
        )

        for item
        in payload.history
    )


    instructions = """
You generate concise faculty handoff notes for the My Campus
personalized learning platform.

The student has reached the Faculty support stage after trying
other learning resources and possibly the AI Tutor.

Your job is NOT to teach the student.

Your job is to prepare a useful handoff for a human faculty member.

STRICT RULES:

1. Write for the faculty member, not for the student.

2. State the current topic.

3. Identify what the student appears to be struggling with.

4. Mention what kinds of explanation the AI Tutor already tried,
but only when that is visible in the conversation.

5. Mention what still appears unclear.

6. Suggest a DIFFERENT teaching approach for faculty when possible.

7. Never invent attempts, mistakes, learning preferences,
symptoms of confusion or resources that are not supported by
the supplied information.

8. Do not claim the student watched a video, completed an
interactive activity or played a game unless the supplied data
explicitly proves that.

9. Keep the handoff concise, normally 80 to 160 words.

10. Do not include greetings, markdown headings or generic filler.

11. Do not say "I am an AI".

Return only the handoff summary.
""".strip()


    ai_input = f"""
CURRENT TOPIC

Topic ID:
{context["topic_id"]}

Topic Title:
{context["topic_title"]}

Topic Description:
{context["topic_description"] or "No description available."}


============================================================
AVAILABLE TOPIC CONTEXT
============================================================

Active Notes sections:
{context["note_sections"]}

Backend learning method types:
{", ".join(context["resource_types"]) if context["resource_types"] else "None listed"}


============================================================
AI TUTOR CONVERSATION
============================================================

{history_text}


============================================================
TASK
============================================================

Create the faculty handoff summary now.

Focus on:
- the student's exact difficulty,
- explanations already attempted,
- remaining confusion,
- a useful different approach the faculty could try.

Do not invent evidence.
""".strip()


    summary = call_openai(
        instructions,
        ai_input,
    )


    if summary:

        provider = "openai"

        model = OPENAI_MODEL


    else:

        provider = (
            "local_handoff_fallback"
        )

        model = None

        summary = (
            build_local_handoff_summary(
                topic.title,
                payload.history,
            )
        )


    summary = clean_text(
        summary
    )


    if not summary:

        summary = (
            build_local_handoff_summary(
                topic.title,
                payload.history,
            )
        )


    return FacultyHandoffResponse(

        summary=summary,

        topic_id=topic.id,

        topic_title=topic.title,

        provider=provider,

        model=model,

        ai_attempted=has_ai_history,
    )


# ============================================================
# CREATE DOUBT
# ============================================================

@router.post(
    "/doubts",
    status_code=201,
)
def create_doubt(

    payload: Doubt,

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    if user.role != "student":

        raise HTTPException(
            403,
            "Student access required",
        )


    topic = topic_access(
        db,
        user,
        payload.topic_id,
    )


    text = (
        payload.doubt_text
        .strip()
    )


    if len(text) < 3:

        raise HTTPException(
            400,
            "Please describe your doubt.",
        )


    return tickets.create_ticket(

        tickets.CreateTicketRequest(

            student_id=user.id,

            subject_id=(
                topic.subject_id
            ),

            level_id=(
                topic.level_id
            ),

            topic_id=(
                topic.id
            ),

            doubt_text=text,

            ai_attempted=(
                payload.ai_attempted
            ),
        ),

        db,
    )


# ============================================================
# TICKET LIST
# ============================================================

@router.get(
    "/tickets"
)
def ticket_list(

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    if user.role == "faculty":

        return (
            tickets
            .get_faculty_tickets(
                user.id,
                db,
            )
        )


    if user.role == "student":

        return (
            tickets
            .get_student_tickets(
                user.id,
                db,
            )
        )


    raise HTTPException(
        403,
        "Access denied",
    )


# ============================================================
# START TICKET
# ============================================================

@router.patch(
    "/tickets/{ticket_id}/start"
)
def start(

    ticket_id: int,

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    faculty(
        user
    )


    return tickets.start_ticket(
        ticket_id,
        user.id,
        db,
    )


# ============================================================
# RESOLVE TICKET
# ============================================================

@router.patch(
    "/tickets/{ticket_id}/resolve"
)
def resolve(

    ticket_id: int,

    payload: Reply,

    user: User = Depends(
        portal_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    faculty(
        user
    )


    response_text = (
        payload.faculty_response
        .strip()
    )


    if len(
        response_text
    ) < 3:

        raise HTTPException(
            400,
            (
                "Please enter "
                "a helpful reply."
            ),
        )


    return tickets.resolve_ticket(

        ticket_id,

        tickets.ResolveTicketRequest(

            faculty_id=user.id,

            faculty_response=(
                response_text
            ),
        ),

        db,
    )