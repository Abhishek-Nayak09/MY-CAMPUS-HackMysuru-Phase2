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
    # FIND TOPIC 1
    # =========================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.title ==
            "Why Physics? & Real-World Applications"
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 1 not found."
        )


    # =========================================================
    # FIND EXISTING VIDEO RESOURCE
    # =========================================================

    video = (
        db.query(LearningContent)
        .filter(
            LearningContent.topic_id == topic.id,
            LearningContent.resource_type == "video"
        )
        .first()
    )


    if not video:

        video = LearningContent(

            topic_id=topic.id,

            resource_type="video",

            title=
                "Physics - Basic Introduction",

            description=
                "A beginner-friendly video lesson introducing the fundamental ideas of Physics.",

            content_text=
                "",

            resource_url=
                "https://www.youtube.com/watch?v=b1t41Q3xRM8",

            content_order=2,

            uploaded_by=None,

            is_active=True
        )


        db.add(video)


    else:

        video.title = (
            "Physics - Basic Introduction"
        )

        video.description = (
            "A beginner-friendly video lesson introducing the fundamental ideas of Physics."
        )

        video.resource_url = (
            "https://www.youtube.com/watch?v=b1t41Q3xRM8"
        )

        video.content_text = """
BEFORE YOU WATCH

Do not try to memorize every formula.

Instead, observe how Physics connects
mathematics with events happening in the real world.


WHAT TO LOOK FOR

1. What does Physics study?

2. How are measurements used in Physics?

3. Why are quantities such as distance,
   speed, velocity, force and energy important?

4. How does Physics allow us to describe
   and predict real-world events?


CONNECT WITH OUR NOTES

While watching, think about:

• Your phone producing sound

• Friction while walking

• Force changing the motion of a car

• Gravity acting on a football

• Light carrying energy

• A rocket producing thrust


AFTER WATCHING

You should be able to explain:

“Physics studies how matter, motion,
forces and energy behave and interact.”

Do not worry if everything is not clear yet.

The Visual Learning and AI Tutor modes
will help explain the difficult parts again.
"""

        video.content_order = 2

        video.is_active = True


    db.commit()

    db.refresh(video)


    # =========================================================
    # VERIFY
    # =========================================================

    print("")
    print("==========================================")
    print(" TOPIC 1 YOUTUBE VIDEO UPDATED")
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
    print("VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()