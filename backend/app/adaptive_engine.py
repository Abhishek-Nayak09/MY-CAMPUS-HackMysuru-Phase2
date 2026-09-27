from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.doubt_ticket import DoubtTicket

from app.models.level_test import (
    LevelTestAnswer,
    LevelTestAttempt,
    LevelTestQuestion,
)

from app.models.personalization import (
    StudentLearningProfile,
    StudentTopicJourney,
    StudentTopicResourceProgress,
)

from app.models.topic import Topic


# ============================================================
# MY CAMPUS ADAPTIVE INTELLIGENCE ENGINE
# VERSION 2.1
# ============================================================

CORE_RESOURCES = [
    "notes",
    "video",
    "interactive",
    "game",
]

SUPPORT_RESOURCES = [
    "ai_tutor",
    "faculty",
]

ALL_RESOURCES = (
    CORE_RESOURCES
    +
    SUPPORT_RESOURCES
)


RESOURCE_LABELS = {

    "notes":
        "Notes",

    "video":
        "Video",

    "interactive":
        "3D Interactive",

    "game":
        "Game",

    "ai_tutor":
        "AI Tutor",

    "faculty":
        "Faculty",

    "next_topic":
        "Continue to Next Topic",
}


# ============================================================
# GENERIC HELPERS
# ============================================================

def clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 1.0,
) -> float:

    return max(
        minimum,
        min(
            maximum,
            value,
        ),
    )


def days_since(
    value: datetime | None,
) -> float:

    if value is None:

        return 999.0


    seconds = (
        datetime.utcnow()
        -
        value
    ).total_seconds()


    if seconds < 0:

        return 0.0


    return (
        seconds
        /
        86400.0
    )


def recency_weight(
    value: datetime | None,
) -> float:

    """
    Recent evidence receives more importance.

    Today:
        approximately 1.0

    30 days:
        approximately 0.5

    Older evidence:
        progressively weaker
    """

    days = days_since(
        value
    )


    return (
        1.0
        /
        (
            1.0
            +
            days
            /
            30.0
        )
    )


def elapsed_minutes(
    start: datetime | None,
    end: datetime | None,
):

    if (
        start is None
        or
        end is None
    ):

        return None


    seconds = (
        end
        -
        start
    ).total_seconds()


    if seconds < 0:

        return None


    return round(
        seconds
        /
        60.0,
        1,
    )


# ============================================================
# LOAD RESOURCE HISTORY
# ============================================================

def load_resource_history(
    db: Session,
    student_id: int,
):

    return (

        db.query(
            StudentTopicResourceProgress
        )

        .filter(
            StudentTopicResourceProgress.student_id
            ==
            student_id
        )

        .order_by(
            StudentTopicResourceProgress.updated_at.asc()
        )

        .all()
    )


# ============================================================
# DETERMINE WHETHER RESOURCE WAS ACTUALLY USED
# ============================================================

def resource_was_attempted(
    row: StudentTopicResourceProgress,
) -> bool:

    return bool(

        int(
            row.visit_count
            or
            0
        )
        >
        0

        or

        row.started_at

        or

        (
            row.status
            and
            row.status
            !=
            "not_started"
        )
    )


# ============================================================
# RESOURCE METRICS
# ============================================================

def calculate_resource_metrics(
    rows: list[
        StudentTopicResourceProgress
    ],
):

    grouped = defaultdict(
        list
    )


    for row in rows:

        grouped[
            row.resource_type
        ].append(
            row
        )


    result = {}


    for resource in ALL_RESOURCES:

        resource_rows = [

            row

            for row
            in grouped.get(
                resource,
                []
            )

            if resource_was_attempted(
                row
            )
        ]


        started_topics = len(
            resource_rows
        )


        successful_rows = [

            row

            for row
            in resource_rows

            if row.understood_here
        ]


        successful_topics = len(
            successful_rows
        )


        raw_success_rate = (

            successful_topics
            /
            started_topics

            if started_topics
            else
            0.0
        )


        # ----------------------------------------------------
        # BAYESIAN-LIKE SMALL SAMPLE CONTROL
        #
        # Prior:
        # 50% expected success
        # strength = 3 observations
        #
        # Prevents:
        # 1 success / 1 attempt = immediate 100% preference
        # ----------------------------------------------------

        prior_strength = 3.0

        prior_successes = (
            prior_strength
            *
            0.5
        )


        posterior_success_rate = (

            (
                successful_topics
                +
                prior_successes
            )
            /
            (
                started_topics
                +
                prior_strength
            )

            if started_topics
            else
            0.0
        )


        # ----------------------------------------------------
        # RECENT PERFORMANCE
        # ----------------------------------------------------

        weighted_attempts = 0.0

        weighted_successes = 0.0


        for row in resource_rows:

            weight = recency_weight(

                row.updated_at
                or
                row.started_at
            )


            weighted_attempts += (
                weight
            )


            if row.understood_here:

                weighted_successes += (
                    weight
                )


        recent_success_rate = (

            weighted_successes
            /
            weighted_attempts

            if weighted_attempts
            >
            0
            else
            0.0
        )


        # ----------------------------------------------------
        # REPEATED FAILURE / FRICTION
        #
        # Only penalize repeated use when the topic
        # was NOT understood.
        #
        # This avoids penalizing successful resources merely
        # because the frontend was opened many times.
        # ----------------------------------------------------

        unresolved_repeat_topics = 0


        for row in resource_rows:

            visits = int(
                row.visit_count
                or
                0
            )


            if (
                visits >= 2
                and
                not row.understood_here
            ):

                unresolved_repeat_topics += 1


        friction_rate = (

            unresolved_repeat_topics
            /
            started_topics

            if started_topics
            else
            0.0
        )


        friction_penalty = min(
            12.0,
            friction_rate
            *
            12.0,
        )


        # ----------------------------------------------------
        # EVIDENCE STRENGTH
        #
        # One successful topic is useful evidence,
        # but not enough to permanently dominate the profile.
        # ----------------------------------------------------

        if started_topics == 0:

            evidence_strength = 0.0

        else:

            evidence_strength = (

                0.45

                +

                0.55
                *
                min(
                    1.0,
                    started_topics
                    /
                    4.0,
                )
            )


        # ----------------------------------------------------
        # EXPERIENCE BONUS
        # ----------------------------------------------------

        experience_bonus = min(
            10.0,
            started_topics
            *
            2.5,
        )


        # ----------------------------------------------------
        # BASE SCORE
        #
        # Historical reliability:
        #     70
        #
        # Recent performance:
        #     20
        #
        # Experience:
        #     10
        #
        # Friction:
        #     negative signal
        # ----------------------------------------------------

        raw_score = (

            posterior_success_rate
            *
            70.0

            +

            recent_success_rate
            *
            20.0

            +

            experience_bonus

            -

            friction_penalty
        )


        adaptive_score = (

            raw_score
            *
            evidence_strength

            if started_topics
            else
            0.0
        )


        adaptive_score = max(
            0.0,
            min(
                100.0,
                adaptive_score,
            ),
        )


        # ----------------------------------------------------
        # RAW ELAPSED TIME
        #
        # We report it for analytics only.
        #
        # IMPORTANT:
        # It is NOT used in preference scoring because
        # browser-open time is not equal to active study time.
        # ----------------------------------------------------

        elapsed_values = []


        for row in successful_rows:

            value = elapsed_minutes(
                row.started_at,
                row.understood_at,
            )


            if value is not None:

                elapsed_values.append(
                    value
                )


        observed_elapsed_minutes = (

            round(
                sum(
                    elapsed_values
                )
                /
                len(
                    elapsed_values
                ),
                1,
            )

            if elapsed_values
            else
            None
        )


        total_visits = sum(

            int(
                row.visit_count
                or
                0
            )

            for row
            in resource_rows
        )


        result[
            resource
        ] = {

            "resource_type":
                resource,

            "label":
                RESOURCE_LABELS[
                    resource
                ],

            "started_topics":
                started_topics,

            "successful_topics":
                successful_topics,

            "total_visits":
                total_visits,

            "raw_success_rate":
                round(
                    raw_success_rate,
                    3,
                ),

            "posterior_success_rate":
                round(
                    posterior_success_rate,
                    3,
                ),

            "recent_success_rate":
                round(
                    recent_success_rate,
                    3,
                ),

            "evidence_strength":
                round(
                    evidence_strength,
                    3,
                ),

            "unresolved_repeat_topics":
                unresolved_repeat_topics,

            "friction_penalty":
                round(
                    friction_penalty,
                    2,
                ),

            "observed_elapsed_minutes":
                observed_elapsed_minutes,

            "elapsed_time_used_for_scoring":
                False,

            "adaptive_score":
                round(
                    adaptive_score,
                    2,
                ),
        }


    return result


# ============================================================
# RANK LEARNING MODALITIES
# ============================================================

def rank_core_resources(
    metrics: dict,
):

    return sorted(

        CORE_RESOURCES,

        key=lambda resource:
            (

                metrics[
                    resource
                ][
                    "adaptive_score"
                ],

                metrics[
                    resource
                ][
                    "evidence_strength"
                ],

                metrics[
                    resource
                ][
                    "successful_topics"
                ],

                -CORE_RESOURCES.index(
                    resource
                ),
            ),

        reverse=True,
    )


# ============================================================
# CONFIDENCE
# ============================================================

def calculate_preference_confidence(
    metrics: dict,
    ranking: list[str],
):

    total_evidence = sum(

        metrics[
            resource
        ][
            "started_topics"
        ]

        for resource
        in CORE_RESOURCES
    )


    if total_evidence == 0:

        return 0.0


    evidence_confidence = clamp(

        total_evidence
        /
        12.0
    )


    best_score = (

        metrics[
            ranking[0]
        ][
            "adaptive_score"
        ]

        if ranking
        else
        0.0
    )


    second_score = (

        metrics[
            ranking[1]
        ][
            "adaptive_score"
        ]

        if len(
            ranking
        )
        >
        1
        else
        0.0
    )


    separation = clamp(

        (
            best_score
            -
            second_score
        )
        /
        25.0
    )


    confidence = (

        evidence_confidence
        *
        0.75

        +

        separation
        *
        0.25
    )


    return round(
        clamp(
            confidence
        ),
        2,
    )


def confidence_label(
    value: float,
):

    if value < 0.30:

        return "learning"


    if value < 0.65:

        return "emerging"


    return "strong"


# ============================================================
# CONCEPT GAP HISTORY
# ============================================================

def load_concept_gaps(
    db: Session,
    student_id: int,
    topic_id: int | None = None,
):

    query = (

        db.query(
            LevelTestAnswer,
            LevelTestQuestion,
        )

        .join(
            LevelTestAttempt,
            LevelTestAnswer.attempt_id
            ==
            LevelTestAttempt.id,
        )

        .join(
            LevelTestQuestion,
            LevelTestAnswer.question_id
            ==
            LevelTestQuestion.id,
        )

        .filter(
            LevelTestAttempt.user_id
            ==
            student_id,

            LevelTestAnswer.is_correct
            ==
            False,
        )
    )


    if topic_id is not None:

        query = query.filter(

            LevelTestQuestion.topic_id
            ==
            topic_id
        )


    rows = (

        query

        .order_by(
            LevelTestAnswer.answered_at.desc()
        )

        .limit(
            40
        )

        .all()
    )


    gaps = {}


    for answer, question in rows:

        concept = (

            answer.concept_gap

            or
            question.concept_gap

            or
            "Concept gap"
        )


        key = (

            question.topic_id,
            concept,
        )


        if key not in gaps:

            topic = db.get(
                Topic,
                question.topic_id,
            )


            gaps[
                key
            ] = {

                "topic_id":
                    question.topic_id,

                "topic_title":
                    (
                        topic.title
                        if topic
                        else None
                    ),

                "concept":
                    concept,

                "wrong_count":
                    0,

                "latest_explanation":
                    (
                        answer.explanation
                        or
                        question.explanation
                    ),
            }


        gaps[
            key
        ][
            "wrong_count"
        ] += 1


    output = list(
        gaps.values()
    )


    output.sort(

        key=lambda item:
            item[
                "wrong_count"
            ],

        reverse=True,
    )


    return output


# ============================================================
# CURRENT TOPIC CONTEXT
# ============================================================

def load_topic_context(
    db: Session,
    student_id: int,
    topic_id: int,
):

    topic = db.get(
        Topic,
        topic_id,
    )


    journey = (

        db.query(
            StudentTopicJourney
        )

        .filter(
            StudentTopicJourney.student_id
            ==
            student_id,

            StudentTopicJourney.topic_id
            ==
            topic_id,
        )

        .first()
    )


    resource_rows = (

        db.query(
            StudentTopicResourceProgress
        )

        .filter(
            StudentTopicResourceProgress.student_id
            ==
            student_id,

            StudentTopicResourceProgress.topic_id
            ==
            topic_id,
        )

        .all()
    )


    latest_ticket = (

        db.query(
            DoubtTicket
        )

        .filter(
            DoubtTicket.student_id
            ==
            student_id,

            DoubtTicket.topic_id
            ==
            topic_id,
        )

        .order_by(
            DoubtTicket.id.desc()
        )

        .first()
    )


    by_resource = {

        row.resource_type:
            row

        for row
        in resource_rows
    }


    tried_resources = []

    repeated_unsuccessful_resources = []

    understood_rows = []


    for resource in ALL_RESOURCES:

        row = by_resource.get(
            resource
        )


        if row is None:

            continue


        if resource_was_attempted(
            row
        ):

            tried_resources.append(
                resource
            )


        if (
            int(
                row.visit_count
                or
                0
            )
            >= 2

            and

            not row.understood_here
        ):

            repeated_unsuccessful_resources.append(
                resource
            )


        if row.understood_here:

            understood_rows.append(
                row
            )


    understood_resource = None


    if understood_rows:

        understood_rows.sort(

            key=lambda row:
                (
                    row.understood_at
                    or
                    row.updated_at
                    or
                    row.started_at
                    or
                    datetime.min
                )
        )


        understood_resource = (
            understood_rows[
                -1
            ].resource_type
        )


    return {

        "topic":
            {

                "id":
                    topic.id
                    if topic
                    else topic_id,

                "title":
                    topic.title
                    if topic
                    else None,
            },

        "journey":
            journey,

        "resource_rows":
            resource_rows,

        "by_resource":
            by_resource,

        "tried_resources":
            tried_resources,

        "repeated_unsuccessful_resources":
            repeated_unsuccessful_resources,

        "understood_resource":
            understood_resource,

        "latest_ticket":
            latest_ticket,
    }


# ============================================================
# DATA QUALITY SIGNALS
# ============================================================

def detect_data_quality_signals(
    topic_context: dict | None,
):

    signals = []


    if topic_context is None:

        return signals


    journey = topic_context[
        "journey"
    ]


    ticket = topic_context[
        "latest_ticket"
    ]


    if (
        journey
        and
        journey.resolved
        and
        ticket
        and
        ticket.status
        not in {
            "resolved",
            "closed",
        }
    ):

        signals.append({

            "type":
                "resolved_topic_with_open_ticket",

            "severity":
                "warning",

            "message":
                (
                    "Topic is marked understood, but the "
                    "latest faculty ticket is still open."
                ),
        })


    return signals


# ============================================================
# SUPPORT STATE
# ============================================================

def calculate_support_state(
    topic_context: dict | None,
):

    if topic_context is None:

        return {

            "level":
                "normal",

            "reason":
                "No topic-specific difficulty state requested.",
        }


    journey = topic_context[
        "journey"
    ]


    ticket = topic_context[
        "latest_ticket"
    ]


    tried = set(
        topic_context[
            "tried_resources"
        ]
    )


    repeated = (
        topic_context[
            "repeated_unsuccessful_resources"
        ]
    )


    if (
        journey
        and
        journey.resolved
    ):

        if (
            ticket
            and
            ticket.status
            not in {
                "resolved",
                "closed",
            }
        ):

            return {

                "level":
                    "resolved_with_open_ticket",

                "reason":
                    (
                        "Learning journey is resolved, "
                        "but a faculty ticket remains open."
                    ),
            }


        return {

            "level":
                "resolved",

            "reason":
                "The learner has already understood this topic.",
        }


    if (
        ticket
        and
        ticket.status
        not in {
            "resolved",
            "closed",
        }
    ):

        return {

            "level":
                "faculty_support",

            "reason":
                "An active faculty escalation already exists.",
        }


    if "ai_tutor" in tried:

        return {

            "level":
                "high",

            "reason":
                (
                    "AI Tutor was already tried and "
                    "the topic is still unresolved."
                ),
        }


    core_tried = [

        resource

        for resource
        in CORE_RESOURCES

        if resource in tried
    ]


    if len(
        core_tried
    ) >= 3:

        return {

            "level":
                "high",

            "reason":
                (
                    "Several learning modalities were tried "
                    "without resolving the topic."
                ),
        }


    if repeated:

        return {

            "level":
                "medium",

            "reason":
                (
                    "At least one learning modality was "
                    "repeated without understanding."
                ),
        }


    if core_tried:

        return {

            "level":
                "light",

            "reason":
                "The learner has started working on this topic.",
        }


    return {

        "level":
            "normal",

        "reason":
            "No strong struggle signal exists yet.",
    }


# ============================================================
# LEARNING STATE
# ============================================================

def detect_learning_state(
    topic_context: dict | None,
    support: dict,
):

    if topic_context is None:

        return "profile_only"


    journey = topic_context[
        "journey"
    ]


    if (
        journey
        and
        journey.resolved
    ):

        return "resolved"


    if support[
        "level"
    ] == "faculty_support":

        return "escalated"


    if support[
        "level"
    ] in {
        "medium",
        "high",
    }:

        return "struggling"


    if topic_context[
        "tried_resources"
    ]:

        return "learning"


    return "new"


# ============================================================
# CHOOSE NEXT ACTION
# ============================================================

def choose_next_action(
    ranking: list[str],
    topic_context: dict | None,
):

    if topic_context is None:

        if ranking:

            return ranking[0]


        return "notes"


    journey = topic_context[
        "journey"
    ]


    # --------------------------------------------------------
    # TOPIC ALREADY UNDERSTOOD
    # --------------------------------------------------------

    if (
        journey
        and
        journey.resolved
    ):

        return "next_topic"


    ticket = topic_context[
        "latest_ticket"
    ]


    # --------------------------------------------------------
    # ACTIVE FACULTY TICKET
    # --------------------------------------------------------

    if (
        ticket
        and
        ticket.status
        not in {
            "resolved",
            "closed",
        }
    ):

        return "faculty"


    tried = set(
        topic_context[
            "tried_resources"
        ]
    )


    repeated = set(
        topic_context[
            "repeated_unsuccessful_resources"
        ]
    )


    # --------------------------------------------------------
    # AI ALREADY TRIED, STILL UNRESOLVED
    # --------------------------------------------------------

    if "ai_tutor" in tried:

        return "faculty"


    # --------------------------------------------------------
    # STRONGEST UNTRIED CORE MODALITY
    # --------------------------------------------------------

    for resource in ranking:

        if (
            resource not in tried
            and
            resource not in repeated
        ):

            return resource


    # --------------------------------------------------------
    # ALL CORE MODES TRIED
    # --------------------------------------------------------

    if all(

        resource in tried

        for resource
        in CORE_RESOURCES
    ):

        return "ai_tutor"


    # --------------------------------------------------------
    # REUSE A SUCCESSFUL MODE IF NEEDED
    # --------------------------------------------------------

    for resource in ranking:

        if resource not in repeated:

            return resource


    return "ai_tutor"


# ============================================================
# EXPLORATION MODE
# ============================================================

def choose_exploration_resource(
    ranking: list[str],
    metrics: dict,
    recommended: str,
):

    if recommended in {
        "next_topic",
        "faculty",
        "ai_tutor",
    }:

        return None


    candidates = [

        resource

        for resource
        in ranking

        if (
            resource
            !=
            recommended

            and

            metrics[
                resource
            ][
                "started_topics"
            ]
            <=
            1
        )
    ]


    if not candidates:

        return None


    return candidates[0]


# ============================================================
# PERSONALIZED SEQUENCE
# ============================================================

def build_personalized_sequence(
    recommended: str,
    ranking: list[str],
):

    if recommended == "next_topic":

        return [
            "next_topic"
        ]


    sequence = []


    if recommended in ALL_RESOURCES:

        sequence.append(
            recommended
        )


    for resource in ranking:

        if resource not in sequence:

            sequence.append(
                resource
            )


    if "ai_tutor" not in sequence:

        sequence.append(
            "ai_tutor"
        )


    if "faculty" not in sequence:

        sequence.append(
            "faculty"
        )


    return sequence


# ============================================================
# LOW EFFECTIVENESS RESOURCE DETECTION
# ============================================================

def detect_low_effectiveness_resources(
    metrics: dict,
):

    result = []


    for resource in CORE_RESOURCES:

        item = metrics[
            resource
        ]


        if (

            item[
                "started_topics"
            ]
            >=
            2

            and

            item[
                "raw_success_rate"
            ]
            <=
            0.25

            and

            item[
                "unresolved_repeat_topics"
            ]
            >=
            1
        ):

            result.append(
                resource
            )


    return result


# ============================================================
# RECOMMENDATION REASONS
# ============================================================

def build_recommendation_reasons(
    recommended: str,
    metrics: dict,
    support: dict,
    concept_gaps: list[dict],
):

    reasons = []


    if recommended == "next_topic":

        reasons.append(
            "This topic is already marked as understood."
        )

        reasons.append(
            "The learner can continue to the next topic."
        )

        return reasons


    if recommended == "faculty":

        reasons.append(
            support[
                "reason"
            ]
        )

        return reasons


    if recommended == "ai_tutor":

        reasons.append(
            "Core learning resources have already been explored."
        )

        reasons.append(
            "AI Tutor is the next adaptive support layer."
        )

        return reasons


    if recommended in metrics:

        item = metrics[
            recommended
        ]


        if item[
            "successful_topics"
        ] > 0:

            reasons.append(

                (
                    f"{item['label']} helped the learner "
                    f"understand {item['successful_topics']} "
                    f"previous topic(s)."
                )
            )


        if item[
            "started_topics"
        ] > 0:

            reasons.append(

                (
                    "Recommendation uses both success rate "
                    "and amount of supporting evidence."
                )
            )


        if item[
            "recent_success_rate"
        ] > 0:

            reasons.append(
                "Recent successful activity receives extra weight."
            )


    if concept_gaps:

        reasons.append(

            (
                f"{len(concept_gaps)} assessment concept-gap "
                "signal(s) are included in this decision."
            )
        )


    if not reasons:

        reasons.append(
            (
                "There is not enough evidence yet, "
                "so the engine is still learning the learner."
            )
        )


    return reasons


# ============================================================
# UPDATE EXISTING PROFILE SUMMARY
# ============================================================

def synchronize_existing_profile(
    db: Session,
    student_id: int,
    ranking: list[str],
    confidence: float,
):

    profile = (

        db.query(
            StudentLearningProfile
        )

        .filter(
            StudentLearningProfile.student_id
            ==
            student_id
        )

        .first()
    )


    if profile is None:

        return None


    best_resource = (

        ranking[0]

        if ranking
        else None
    )


    profile.preferred_resource = (
        best_resource
    )


    profile.preference_confidence = (
        confidence
    )


    return profile


# ============================================================
# MAIN ENGINE
# ============================================================

def build_adaptive_snapshot(
    db: Session,
    student_id: int,
    topic_id: int | None = None,
):

    # --------------------------------------------------------
    # 1. COMPLETE RESOURCE HISTORY
    # --------------------------------------------------------

    resource_history = load_resource_history(
        db,
        student_id,
    )


    # --------------------------------------------------------
    # 2. RESOURCE EFFECTIVENESS
    # --------------------------------------------------------

    metrics = calculate_resource_metrics(
        resource_history
    )


    # --------------------------------------------------------
    # 3. LEARNING MODALITY RANKING
    # --------------------------------------------------------

    ranking = rank_core_resources(
        metrics
    )


    # --------------------------------------------------------
    # 4. CONFIDENCE
    # --------------------------------------------------------

    confidence = (
        calculate_preference_confidence(
            metrics,
            ranking,
        )
    )


    # --------------------------------------------------------
    # 5. CURRENT TOPIC CONTEXT
    # --------------------------------------------------------

    topic_context = None


    if topic_id is not None:

        topic_context = load_topic_context(
            db,
            student_id,
            topic_id,
        )


    # --------------------------------------------------------
    # 6. CONCEPT GAPS
    # --------------------------------------------------------

    concept_gaps = load_concept_gaps(
        db,
        student_id,
        topic_id,
    )


    # --------------------------------------------------------
    # 7. SUPPORT STATE
    # --------------------------------------------------------

    support = calculate_support_state(
        topic_context
    )


    # --------------------------------------------------------
    # 8. LEARNING STATE
    # --------------------------------------------------------

    learning_state = detect_learning_state(
        topic_context,
        support,
    )


    # --------------------------------------------------------
    # 9. NEXT ACTION
    # --------------------------------------------------------

    recommended = choose_next_action(
        ranking,
        topic_context,
    )


    # --------------------------------------------------------
    # 10. EXPLORATION
    # --------------------------------------------------------

    exploration = (
        choose_exploration_resource(
            ranking,
            metrics,
            recommended,
        )
    )


    # --------------------------------------------------------
    # 11. PERSONALIZED RESOURCE SEQUENCE
    # --------------------------------------------------------

    sequence = (
        build_personalized_sequence(
            recommended,
            ranking,
        )
    )


    # --------------------------------------------------------
    # 12. LOW-EFFECTIVENESS MODES
    # --------------------------------------------------------

    low_effectiveness = (
        detect_low_effectiveness_resources(
            metrics
        )
    )


    # --------------------------------------------------------
    # 13. DATA QUALITY
    # --------------------------------------------------------

    data_quality_signals = (
        detect_data_quality_signals(
            topic_context
        )
    )


    # --------------------------------------------------------
    # 14. SYNCHRONIZE EXISTING PROFILE
    # --------------------------------------------------------

    profile = synchronize_existing_profile(
        db,
        student_id,
        ranking,
        confidence,
    )


    if profile:

        db.flush()


    # --------------------------------------------------------
    # 15. CURRENT TOPIC PAYLOAD
    # --------------------------------------------------------

    current_topic = None


    if topic_context:

        journey = topic_context[
            "journey"
        ]


        ticket = topic_context[
            "latest_ticket"
        ]


        current_topic = {

            "id":
                topic_context[
                    "topic"
                ][
                    "id"
                ],

            "title":
                topic_context[
                    "topic"
                ][
                    "title"
                ],

            "learning_state":
                learning_state,

            "tried_resources":
                topic_context[
                    "tried_resources"
                ],

            "repeated_unsuccessful_resources":
                topic_context[
                    "repeated_unsuccessful_resources"
                ],

            "understood_resource":
                topic_context[
                    "understood_resource"
                ],

            "resolved":
                bool(
                    journey
                    and
                    journey.resolved
                ),

            "resolved_resource":
                (
                    journey.resolved_resource
                    if journey
                    else None
                ),

            "faculty_ticket_status":
                (
                    ticket.status
                    if ticket
                    else None
                ),
        }


    # --------------------------------------------------------
    # 16. HISTORY SUMMARY
    # --------------------------------------------------------

    topics_understood = (

        int(
            profile.topics_understood
            or
            0
        )

        if profile
        else 0
    )


    faculty_escalations = (

        int(
            profile.faculty_escalations
            or
            0
        )

        if profile
        else 0
    )


    total_resource_visits = sum(

        metrics[
            resource
        ][
            "total_visits"
        ]

        for resource
        in ALL_RESOURCES
    )


    total_core_evidence = sum(

        metrics[
            resource
        ][
            "started_topics"
        ]

        for resource
        in CORE_RESOURCES
    )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "student_id":
            student_id,

        "engine":
            {

                "name":
                    "MY CAMPUS Adaptive Intelligence Engine",

                "version":
                    "2.1",

                "mode":
                    "dynamic_evidence_profile",

                "principles": [

                    "recent evidence weighted",

                    "small-sample protection",

                    "repeated-failure detection",

                    "concept-gap awareness",

                    "support escalation",

                    "exploration without learner locking",
                ],
            },

        "learner_model":
            {

                "preferred_resource":
                    (
                        ranking[0]
                        if ranking
                        else None
                    ),

                "preferred_resource_label":
                    (
                        RESOURCE_LABELS.get(
                            ranking[0]
                        )
                        if ranking
                        else None
                    ),

                "confidence":
                    confidence,

                "confidence_label":
                    confidence_label(
                        confidence
                    ),

                "ranking":
                    [

                        {
                            "resource_type":
                                resource,

                            "label":
                                RESOURCE_LABELS[
                                    resource
                                ],

                            "adaptive_score":
                                metrics[
                                    resource
                                ][
                                    "adaptive_score"
                                ],

                            "evidence_strength":
                                metrics[
                                    resource
                                ][
                                    "evidence_strength"
                                ],
                        }

                        for resource
                        in ranking
                    ],
            },

        "recommendation":
            {

                "action":
                    recommended,

                "resource_type":
                    (
                        recommended
                        if recommended
                        !=
                        "next_topic"
                        else None
                    ),

                "label":
                    RESOURCE_LABELS[
                        recommended
                    ],

                "confidence":
                    confidence,

                "confidence_label":
                    confidence_label(
                        confidence
                    ),

                "reasons":
                    build_recommendation_reasons(
                        recommended,
                        metrics,
                        support,
                        concept_gaps,
                    ),

                "exploration_resource":
                    exploration,

                "exploration_label":
                    (
                        RESOURCE_LABELS[
                            exploration
                        ]
                        if exploration
                        else None
                    ),
            },

        "personalized_sequence":
            [

                {
                    "resource_type":
                        resource,

                    "label":
                        RESOURCE_LABELS[
                            resource
                        ],
                }

                for resource
                in sequence
            ],

        "support":
            support,

        "current_topic":
            current_topic,

        "active_concept_gaps":
            concept_gaps,

        "low_effectiveness_resources":
            [

                {
                    "resource_type":
                        resource,

                    "label":
                        RESOURCE_LABELS[
                            resource
                        ],

                    "reason":
                        (
                            "Repeated use with low observed "
                            "understanding success."
                        ),
                }

                for resource
                in low_effectiveness
            ],

        "data_quality_signals":
            data_quality_signals,

        "resource_metrics":
            metrics,

        "history_summary":
            {

                "topics_understood":
                    topics_understood,

                "faculty_escalations":
                    faculty_escalations,

                "total_resource_visits":
                    total_resource_visits,

                "core_learning_evidence":
                    total_core_evidence,

                "concept_gap_count":
                    len(
                        concept_gaps
                    ),
            },

        "generated_at":
            datetime.utcnow(),
    }