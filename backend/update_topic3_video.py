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
    # TOPIC 3
    # Use ID directly to avoid apostrophe/title mismatch
    # =========================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == 3
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 3 not found."
        )


    # =========================================================
    # VIDEO DETAILS
    # =========================================================

    video_title = (
        "Newton's Laws of Motion"
    )


    video_description = (
        "A guided Physics lesson covering Newton's First, "
        "Second and Third Laws with force, inertia, "
        "acceleration and action-reaction concepts."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=g550H4e5FCY"
    )


    learning_guide = """
BEFORE YOU WATCH

You already studied Forces and Newton's Laws
using our Rich Notes.

While watching this video,
do not focus only on memorizing the three laws.

Try to understand:

WHY an object changes motion
and
WHAT force causes that change.


WHAT TO LOOK FOR

1. What is a force?

2. What happens when the net force is zero?

3. What exactly is inertia?

4. How are force, mass and acceleration related?

5. What does F = ma actually mean?

6. Why do action and reaction forces not cancel each other?

7. Where do we see Newton's Laws in everyday life?


NEWTON'S FIRST LAW

An object tends to keep its current state of motion
unless a net external force acts on it.

KEY CONCEPT:

INERTIA


REAL-WORLD CONNECTION

Imagine travelling inside a moving bus.

The bus suddenly stops.

Your body tends to continue moving forward.

Why?

Your body was already moving.

It resists the sudden change in motion.

That tendency is called inertia.


CONNECT WITH THE NOTES

Car moving
→ passenger moving with car

Car suddenly brakes
→ car slows down

Passenger tends to continue forward
→ inertia

Seat belt provides the force
needed to stop the passenger safely.


NEWTON'S SECOND LAW

The relationship between force,
mass and acceleration is:

F = m × a


WHAT DOES THIS TELL US?

For the same mass:

More Force
→ More Acceleration


For the same force:

More Mass
→ Less Acceleration


EXAMPLE

Mass = 5 kg

Acceleration = 2 m/s²


F = m × a

F = 5 × 2

F = 10 N


REAL-WORLD CONNECTION

Compare:

An empty shopping cart

and

A heavily loaded shopping cart.


Using the same pushing force:

The lighter cart accelerates more easily.

The heavier cart accelerates less.

The reason is its greater mass.


NEWTON'S THIRD LAW

For every action,
there is an equal and opposite reaction.


IMPORTANT

The two forces:

• Are equal in magnitude
• Are opposite in direction
• Act on DIFFERENT objects


EXAMPLE — WALKING

Your foot pushes the ground backward.

The ground pushes your foot forward.

That forward reaction helps you walk.


EXAMPLE — SWIMMING

Swimmer pushes water backward.

Water pushes swimmer forward.


EXAMPLE — ROCKET

Rocket pushes exhaust gases downward.

Exhaust gases push rocket upward.

That reaction force produces thrust.


BALANCED VS UNBALANCED FORCES

BALANCED:

Net Force = 0

No acceleration.


UNBALANCED:

Net Force is not zero.

Acceleration occurs.


ENGINEERING CONNECTION

Newton's Laws are used in:

• Vehicle design
• Braking systems
• Robotics
• Machines
• Elevators
• Aircraft
• Rockets
• Structural engineering
• Sports analysis


AFTER WATCHING

You should be able to explain:


LAW 1

Why does a passenger move forward
when a car suddenly brakes?

Answer:

Inertia.


LAW 2

What happens if force increases
while mass remains constant?

Answer:

Acceleration increases.


LAW 3

Why can a swimmer move forward
by pushing water backward?

Answer:

The water provides an equal and opposite
reaction force.


SELF CHECK

Question:

A 4 kg object accelerates at 3 m/s².

What is the net force?


Use:

F = m × a


F = 4 × 3

F = 12 N


FINAL CONNECTION

Newton's First Law
→ What happens when net force is zero?


Newton's Second Law
→ What happens when net force acts?


Newton's Third Law
→ How two interacting objects exert forces
on each other.


KEY TAKEAWAY

No net force
→ No change in velocity

Net force
→ Acceleration

F = ma
→ Force controls acceleration

Interaction
→ Equal and opposite force pair
"""


    # =========================================================
    # FIND EXISTING TOPIC 3 VIDEO
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
    # CREATE
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


    # =========================================================
    # UPDATE
    # =========================================================

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


    # =========================================================
    # SAVE
    # =========================================================

    db.commit()

    db.refresh(video)


    # =========================================================
    # VERIFY
    # =========================================================

    print("")
    print("==========================================")
    print(" TOPIC 3 YOUTUBE VIDEO UPDATED")
    print("==========================================")
    print("")

    print(
        f"Topic ID : {topic.id}"
    )

    print(
        f"Topic    : {topic.title}"
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
    print("TOPIC 3 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()