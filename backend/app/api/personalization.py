
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.topic import Topic

from app.models.personalization import (
    StudentLearningProfile,
    StudentTopicJourney,
    StudentTopicResourceProgress,
)


router = APIRouter(
    prefix="/personalization",
    tags=["Student Personalization"]
)


RESOURCE_ORDER = [
    "notes",
    "video",
    "interactive",
    "game",
    "ai_tutor",
    "faculty",
]


RESOURCE_LABELS = {
    "notes":
        "Notes",

    "video":
        "Video",

    "interactive":
        "Interactive / Graphs",

    "game":
        "Game",

    "ai_tutor":
        "AI Tutor",

    "faculty":
        "Faculty",
}


ATTEMPT_FIELDS = {
    "notes":
        "notes_attempts",

    "video":
        "video_attempts",

    "interactive":
        "interactive_attempts",

    "game":
        "game_attempts",

    "ai_tutor":
        "ai_tutor_attempts",

    "faculty":
        "faculty_attempts",
}


SUCCESS_FIELDS = {
    "notes":
        "notes_understood",

    "video":
        "video_understood",

    "interactive":
        "interactive_understood",

    "game":
        "game_understood",

    "ai_tutor":
        "ai_tutor_understood",

    "faculty":
        "faculty_resolved",
}


# ============================================================
# SCHEMAS
# ============================================================

class ResourceEventRequest(BaseModel):

    student_id: int

    topic_id: int

    resource_type: str

    event: str


class StartRecommendationRequest(BaseModel):

    student_id: int

    topic_id: int


# ============================================================
# HELPERS
# ============================================================

def normalize_resource(
    value: str
) -> str:

    value = (
        str(
            value
            or ""
        )
        .strip()
        .lower()
        .replace(
            "-",
            "_"
        )
        .replace(
            " ",
            "_"
        )
    )


    aliases = {

        "note":
            "notes",

        "notes":
            "notes",

        "videos":
            "video",

        "video":
            "video",

        "interaction":
            "interactive",

        "interactive":
            "interactive",

        "graph":
            "interactive",

        "graphs":
            "interactive",

        "simulation":
            "interactive",

        "simulations":
            "interactive",

        "game":
            "game",

        "games":
            "game",

        "ai":
            "ai_tutor",

        "ai_tutor":
            "ai_tutor",

        "aitutor":
            "ai_tutor",

        "faculty":
            "faculty",
    }


    normalized = aliases.get(
        value
    )


    if (
        normalized
        not in RESOURCE_ORDER
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid resource type. "
                "Use notes, video, interactive, "
                "game, ai_tutor or faculty."
            )
        )


    return normalized


def normalize_event(
    value: str
) -> str:

    value = (
        str(
            value
            or ""
        )
        .strip()
        .lower()
        .replace(
            "-",
            "_"
        )
        .replace(
            " ",
            "_"
        )
    )


    aliases = {

        "start":
            "started",

        "started":
            "started",

        "open":
            "started",

        "opened":
            "started",

        "complete":
            "completed",

        "completed":
            "completed",

        "next":
            "next",

        "understand":
            "understood",

        "understood":
            "understood",

        "i_understood":
            "understood",

        "faculty_escalated":
            "faculty_escalated",

        "escalated":
            "faculty_escalated",
    }


    normalized = aliases.get(
        value
    )


    if normalized is None:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid event. "
                "Use started, completed, next, "
                "understood or faculty_escalated."
            )
        )


    return normalized


def get_topic_or_404(
    db: Session,
    topic_id: int
):

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )


    if not topic:

        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )


    return topic


def get_or_create_profile(
    db: Session,
    student_id: int
):

    profile = (
        db.query(
            StudentLearningProfile
        )
        .filter(
            StudentLearningProfile.student_id
            == student_id
        )
        .first()
    )


    if profile:

        return profile


    profile = StudentLearningProfile(
        student_id=student_id
    )


    db.add(
        profile
    )


    db.flush()


    return profile


def get_or_create_journey(
    db: Session,
    student_id: int,
    topic_id: int
):

    journey = (
        db.query(
            StudentTopicJourney
        )
        .filter(
            StudentTopicJourney.student_id
            == student_id,

            StudentTopicJourney.topic_id
            == topic_id
        )
        .first()
    )


    if journey:

        return journey


    journey = StudentTopicJourney(
        student_id=student_id,
        topic_id=topic_id,
        current_resource="notes"
    )


    db.add(
        journey
    )


    db.flush()


    return journey


def get_or_create_progress(
    db: Session,
    student_id: int,
    topic_id: int,
    resource_type: str
):

    progress = (
        db.query(
            StudentTopicResourceProgress
        )
        .filter(
            StudentTopicResourceProgress.student_id
            == student_id,

            StudentTopicResourceProgress.topic_id
            == topic_id,

            StudentTopicResourceProgress.resource_type
            == resource_type
        )
        .first()
    )


    created = False


    if progress is None:

        progress = StudentTopicResourceProgress(
            student_id=student_id,
            topic_id=topic_id,
            resource_type=resource_type,
            status="not_started"
        )


        db.add(
            progress
        )


        db.flush()


        created = True


    return (
        progress,
        created
    )


def next_resource_after(
    resource_type: str
):

    index = RESOURCE_ORDER.index(
        resource_type
    )


    if (
        index + 1
        >= len(
            RESOURCE_ORDER
        )
    ):

        return None


    return RESOURCE_ORDER[
        index + 1
    ]


def recalculate_profile(
    profile: StudentLearningProfile
):

    total_successes = 0

    scores = {}


    for resource in RESOURCE_ORDER:

        attempt_field = (
            ATTEMPT_FIELDS[
                resource
            ]
        )


        success_field = (
            SUCCESS_FIELDS[
                resource
            ]
        )


        attempts = int(
            getattr(
                profile,
                attempt_field
            )
            or 0
        )


        successes = int(
            getattr(
                profile,
                success_field
            )
            or 0
        )


        total_successes += (
            successes
        )


        success_rate = (
            successes
            /
            attempts
            if attempts > 0
            else 0.0
        )


        score = (
            successes
            * 3.0
            +
            success_rate
        )


        if (
            profile.last_successful_resource
            == resource
        ):

            score += 0.35


        scores[
            resource
        ] = {
            "attempts":
                attempts,

            "successes":
                successes,

            "success_rate":
                round(
                    success_rate,
                    3
                ),

            "score":
                round(
                    score,
                    3
                )
        }


    successful_resources = [
        resource
        for resource
        in RESOURCE_ORDER
        if scores[
            resource
        ][
            "successes"
        ] > 0
    ]


    if not successful_resources:

        profile.preferred_resource = (
            None
        )

        profile.preference_confidence = (
            0.0
        )

        return scores


    best_resource = max(
        successful_resources,
        key=lambda resource: (
            scores[
                resource
            ][
                "score"
            ],

            scores[
                resource
            ][
                "successes"
            ]
        )
    )


    profile.preferred_resource = (
        best_resource
    )


    confidence = min(
        1.0,
        total_successes
        /
        4.0
    )


    profile.preference_confidence = (
        round(
            confidence,
            2
        )
    )


    return scores


def profile_payload(
    profile: StudentLearningProfile
):

    modality_stats = (
        recalculate_profile(
            profile
        )
    )


    preferred = (
        profile.preferred_resource
    )


    if (
        profile.preference_confidence
        < 0.34
    ):

        confidence_label = (
            "early"
        )


    elif (
        profile.preference_confidence
        < 0.75
    ):

        confidence_label = (
            "growing"
        )


    else:

        confidence_label = (
            "strong"
        )


    return {

        "student_id":
            profile.student_id,

        "preferred_resource":
            preferred,

        "preferred_resource_label":
            (
                RESOURCE_LABELS.get(
                    preferred
                )
                if preferred
                else None
            ),

        "preference_confidence":
            profile.preference_confidence,

        "confidence_label":
            confidence_label,

        "last_successful_resource":
            profile.last_successful_resource,

        "topics_understood":
            profile.topics_understood,

        "faculty_escalations":
            profile.faculty_escalations,

        "modalities":
            modality_stats,
    }


def roadmap_payload(
    db: Session,
    student_id: int,
    topic_id: int
):

    rows = (
        db.query(
            StudentTopicResourceProgress
        )
        .filter(
            StudentTopicResourceProgress.student_id
            == student_id,

            StudentTopicResourceProgress.topic_id
            == topic_id
        )
        .all()
    )


    by_resource = {
        row.resource_type:
            row
        for row
        in rows
    }


    roadmap = []


    for resource in RESOURCE_ORDER:

        row = by_resource.get(
            resource
        )


        roadmap.append(
            {
                "resource_type":
                    resource,

                "label":
                    RESOURCE_LABELS[
                        resource
                    ],

                "status":
                    (
                        row.status
                        if row
                        else "not_started"
                    ),

                "visit_count":
                    (
                        row.visit_count
                        if row
                        else 0
                    ),

                "understood_here":
                    (
                        bool(
                            row.understood_here
                        )
                        if row
                        else False
                    )
            }
        )


    return roadmap


# ============================================================
# RESOURCE EVENT
# ============================================================

@router.post("/resource-event")
def resource_event(
    request: ResourceEventRequest,
    db: Session = Depends(get_db)
):

    get_topic_or_404(
        db,
        request.topic_id
    )


    resource = normalize_resource(
        request.resource_type
    )


    event = normalize_event(
        request.event
    )


    profile = get_or_create_profile(
        db,
        request.student_id
    )


    journey = get_or_create_journey(
        db,
        request.student_id,
        request.topic_id
    )


    progress, created = (
        get_or_create_progress(
            db,
            request.student_id,
            request.topic_id,
            resource
        )
    )


    now = datetime.utcnow()


    # --------------------------------------------------------
    # FIRST RESOURCE ATTEMPT
    # --------------------------------------------------------

    if (
        created
        or progress.visit_count == 0
    ):

        attempt_field = (
            ATTEMPT_FIELDS[
                resource
            ]
        )


        setattr(
            profile,
            attempt_field,
            int(
                getattr(
                    profile,
                    attempt_field
                )
                or 0
            )
            + 1
        )


    # --------------------------------------------------------
    # STARTED
    # --------------------------------------------------------

    if event == "started":

        progress.visit_count = (
            int(
                progress.visit_count
                or 0
            )
            + 1
        )


        if progress.started_at is None:

            progress.started_at = (
                now
            )


        if not progress.understood_here:

            progress.status = (
                "started"
            )


        journey.current_resource = (
            resource
        )


    # --------------------------------------------------------
    # COMPLETED
    # --------------------------------------------------------

    elif event == "completed":

        if progress.started_at is None:

            progress.started_at = (
                now
            )


        progress.completed_at = (
            now
        )


        if not progress.understood_here:

            progress.status = (
                "completed"
            )


        journey.current_resource = (
            resource
        )


    # --------------------------------------------------------
    # NEXT RESOURCE
    # --------------------------------------------------------

    elif event == "next":

        if progress.started_at is None:

            progress.started_at = (
                now
            )


        progress.completed_at = (
            now
        )


        if not progress.understood_here:

            progress.status = (
                "completed"
            )


        next_resource = (
            next_resource_after(
                resource
            )
        )


        if next_resource:

            journey.current_resource = (
                next_resource
            )


    # --------------------------------------------------------
    # UNDERSTOOD HERE
    # --------------------------------------------------------

    elif event == "understood":

        already_understood = bool(
            progress.understood_here
        )


        topic_was_resolved = bool(
            journey.resolved
        )


        progress.started_at = (
            progress.started_at
            or now
        )


        progress.completed_at = (
            progress.completed_at
            or now
        )


        progress.understood_at = (
            now
        )


        progress.understood_here = (
            True
        )


        progress.status = (
            "understood"
        )


        journey.current_resource = (
            resource
        )


        journey.resolved = (
            True
        )


        journey.resolved_resource = (
            resource
        )


        journey.resolved_at = (
            now
        )


        if not already_understood:

            success_field = (
                SUCCESS_FIELDS[
                    resource
                ]
            )


            setattr(
                profile,
                success_field,
                int(
                    getattr(
                        profile,
                        success_field
                    )
                    or 0
                )
                + 1
            )


            profile.last_successful_resource = (
                resource
            )


        if not topic_was_resolved:

            profile.topics_understood = (
                int(
                    profile.topics_understood
                    or 0
                )
                + 1
            )


    # --------------------------------------------------------
    # FACULTY ESCALATION
    # --------------------------------------------------------

    elif event == "faculty_escalated":

        progress.status = (
            "escalated"
        )


        journey.current_resource = (
            "faculty"
        )


        profile.faculty_escalations = (
            int(
                profile.faculty_escalations
                or 0
            )
            + 1
        )


    recalculate_profile(
        profile
    )


    db.commit()


    db.refresh(
        profile
    )


    db.refresh(
        journey
    )


    db.refresh(
        progress
    )


    return {

        "status":
            "saved",

        "event":
            event,

        "resource_type":
            resource,

        "resource_label":
            RESOURCE_LABELS[
                resource
            ],

        "next_resource":
            (
                next_resource_after(
                    resource
                )
                if event
                in {
                    "next",
                    "completed"
                }
                else None
            ),

        "topic_resolved":
            journey.resolved,

        "resolved_resource":
            journey.resolved_resource,

        "preferred_resource":
            profile.preferred_resource,

        "preferred_resource_label":
            (
                RESOURCE_LABELS.get(
                    profile.preferred_resource
                )
                if profile.preferred_resource
                else None
            ),

        "preference_confidence":
            profile.preference_confidence,
    }


# ============================================================
# STUDENT PROFILE
# ============================================================

@router.get("/profile/{student_id}")
def get_student_profile(
    student_id: int,
    db: Session = Depends(get_db)
):

    profile = get_or_create_profile(
        db,
        student_id
    )


    payload = profile_payload(
        profile
    )


    db.commit()


    return payload


# ============================================================
# TOPIC JOURNEY + ROADMAP
# ============================================================

@router.get(
    "/topic/{student_id}/{topic_id}"
)
def get_topic_journey(
    student_id: int,
    topic_id: int,
    db: Session = Depends(get_db)
):

    topic = get_topic_or_404(
        db,
        topic_id
    )


    profile = get_or_create_profile(
        db,
        student_id
    )


    journey = get_or_create_journey(
        db,
        student_id,
        topic_id
    )


    profile_info = profile_payload(
        profile
    )


    roadmap = roadmap_payload(
        db,
        student_id,
        topic_id
    )


    has_activity = any(
        item[
            "status"
        ]
        != "not_started"
        for item
        in roadmap
    )


    preferred = (
        profile.preferred_resource
    )


    should_recommend = (
        not journey.resolved
        and not has_activity
        and preferred is not None
        and preferred != "notes"
    )


    recommendation_message = None


    if should_recommend:

        recommendation_message = (
            "You seem to understand concepts "
            f"better through "
            f"{RESOURCE_LABELS[preferred]}. "
            "Would you like to start this "
            "topic there?"
        )


    db.commit()


    return {

        "student_id":
            student_id,

        "topic": {
            "id":
                topic.id,

            "title":
                topic.title,
        },

        "current_resource":
            journey.current_resource,

        "resolved":
            journey.resolved,

        "resolved_resource":
            journey.resolved_resource,

        "roadmap":
            roadmap,

        "personalization": {
            "preferred_resource":
                preferred,

            "preferred_resource_label":
                (
                    RESOURCE_LABELS.get(
                        preferred
                    )
                    if preferred
                    else None
                ),

            "preference_confidence":
                profile.preference_confidence,

            "should_recommend_start":
                should_recommend,

            "recommendation_message":
                recommendation_message,
        },

        "profile":
            profile_info,
    }


# ============================================================
# NEXT-TOPIC START RECOMMENDATION
# ============================================================

@router.post("/start-recommendation")
def start_recommendation(
    request: StartRecommendationRequest,
    db: Session = Depends(get_db)
):

    get_topic_or_404(
        db,
        request.topic_id
    )


    profile = get_or_create_profile(
        db,
        request.student_id
    )


    journey = get_or_create_journey(
        db,
        request.student_id,
        request.topic_id
    )


    preferred = (
        profile.preferred_resource
    )


    if (
        preferred
        and preferred != "notes"
        and not journey.resolved
    ):

        return {

            "recommended":
                True,

            "resource_type":
                preferred,

            "resource_label":
                RESOURCE_LABELS[
                    preferred
                ],

            "message":
                (
                    "You seem to understand "
                    "concepts better through "
                    f"{RESOURCE_LABELS[preferred]}. "
                    "You can start this topic "
                    "with that learning mode."
                ),

            "confidence":
                profile.preference_confidence,
        }


    return {

        "recommended":
            False,

        "resource_type":
            "notes",

        "resource_label":
            "Notes",

        "message":
            (
                "Start with the normal "
                "learning flow."
            ),

        "confidence":
            profile.preference_confidence,
    }


# ============================================================
# FACULTY HANDOFF RAW DATA
# AI SUMMARY WILL BE BUILT ON TOP OF THIS LATER
# ============================================================

@router.get(
    "/faculty-handoff-data/{student_id}/{topic_id}"
)
def faculty_handoff_data(
    student_id: int,
    topic_id: int,
    db: Session = Depends(get_db)
):

    topic = get_topic_or_404(
        db,
        topic_id
    )


    profile = get_or_create_profile(
        db,
        student_id
    )


    journey = get_or_create_journey(
        db,
        student_id,
        topic_id
    )


    roadmap = roadmap_payload(
        db,
        student_id,
        topic_id
    )


    tried_resources = [
        item
        for item
        in roadmap
        if item[
            "status"
        ]
        != "not_started"
    ]


    db.commit()


    return {

        "student_id":
            student_id,

        "topic": {
            "id":
                topic.id,

            "title":
                topic.title,
        },

        "topic_resolved":
            journey.resolved,

        "resolved_resource":
            journey.resolved_resource,

        "current_resource":
            journey.current_resource,

        "resources_tried":
            tried_resources,

        "learning_profile":
            profile_payload(
                profile
            ),

        "handoff_status":
            "raw_data_ready",

        "note":
            (
                "AI-generated faculty handoff "
                "summary will use this journey "
                "data plus AI Tutor conversation "
                "history in the next implementation step."
            ),
    }
