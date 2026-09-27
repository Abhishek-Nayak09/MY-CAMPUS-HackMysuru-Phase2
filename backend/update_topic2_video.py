from app.db.database import SessionLocal

from app.models.user import User
from app.models.course import Course
from app.models.year import AcademicYear
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic
from app.models.learning_content import LearningContent


db = SessionLocal()


try:

    # =========================================================
    # FIND TOPIC 2
    # =========================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.title ==
            "Motion, Distance, Speed & Velocity"
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 2 not found."
        )


    # =========================================================
    # FIND EXISTING VIDEO
    # =========================================================

    video = (
        db.query(LearningContent)
        .filter(
            LearningContent.topic_id == topic.id,
            LearningContent.resource_type == "video"
        )
        .first()
    )


    # =========================================================
    # VIDEO DETAILS
    # =========================================================

    video_title = (
        "Speed, Velocity, Distance & Displacement"
    )


    video_description = (
        "A clear Physics lesson explaining distance, displacement, "
        "speed, velocity, scalar and vector quantities."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=NZvMXcIztuU"
    )


    learning_guide = """
BEFORE YOU WATCH

You already learned these ideas in the Rich Notes.

Now use the video to strengthen the connection between:

• Motion
• Distance
• Displacement
• Speed
• Velocity
• Scalar quantities
• Vector quantities


WHAT TO LOOK FOR

1. Why is distance a scalar quantity?

2. Why is displacement a vector quantity?

3. What is the difference between speed and velocity?

4. Why does velocity need direction?

5. How do we calculate speed?

6. How do we calculate velocity?

7. What does average speed mean for a complete journey?


IMPORTANT FORMULAS

Speed
=
Distance / Time


Velocity
=
Displacement / Time


Average Speed
=
Total Distance / Total Time


CONNECT WITH OUR NOTES

Think about the Home → College example.

If you travel along a curved road:

The complete road travelled represents DISTANCE.

The shortest straight-line change from home
to college represents DISPLACEMENT.


Now think about a car.

60 km/h

This is SPEED.


60 km/h EAST

This is VELOCITY.


REAL-WORLD CONNECTION

While watching, connect these concepts with:

• Car speedometers
• Google Maps
• Running and sports
• Aircraft navigation
• Robot movement
• GPS tracking


AFTER WATCHING

You should be able to explain these four statements:

1. Distance is the total path travelled.

2. Displacement is the straight-line change in position
   with direction.

3. Speed tells how fast an object moves.

4. Velocity tells how fast an object moves
   AND in which direction.


SELF CHECK

Ask yourself:

“If two cars travel at the same speed
but in opposite directions,
do they have the same velocity?”

Answer:

No.

Their speeds may be equal,
but their velocities are different
because their directions are different.


KEY TAKEAWAY

Distance → total path

Displacement → change in position + direction

Speed → distance / time

Velocity → displacement / time + direction
"""


    # =========================================================
    # CREATE / UPDATE
    # =========================================================

    if not video:

        video = LearningContent(

            topic_id=
                topic.id,

            resource_type=
                "video",

            title=
                video_title,

            description=
                video_description,

            content_text=
                learning_guide,

            resource_url=
                youtube_url,

            content_order=
                2,

            uploaded_by=
                None,

            is_active=
                True
        )


        db.add(video)


    else:

        video.title = (
            video_title
        )

        video.description = (
            video_description
        )

        video.content_text = (
            learning_guide
        )

        video.resource_url = (
            youtube_url
        )

        video.content_order = (
            2
        )

        video.is_active = (
            True
        )


    db.commit()

    db.refresh(video)


    # =========================================================
    # VERIFY
    # =========================================================

    print("")
    print("==========================================")
    print(" TOPIC 2 YOUTUBE VIDEO UPDATED")
    print("==========================================")
    print("")

    print(
        f"Topic ID : {topic.id}"
    )

    print(
        f"Video ID : {video.id}"
    )

    print(
        f"Title    : {video.title}"
    )

    print(
        f"URL      : {video.resource_url}"
    )

    print(
        f"Active   : {video.is_active}"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 2 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()