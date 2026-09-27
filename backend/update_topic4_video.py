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
    # TOPIC 4
    # =========================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == 4
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 4 not found."
        )


    # =========================================================
    # VIDEO DETAILS
    # =========================================================

    video_title = (
        "Work, Energy, and Power - Basic Introduction"
    )


    video_description = (
        "A beginner-friendly Physics lesson covering work, "
        "kinetic energy, potential energy, conservation of energy "
        "and power with worked examples."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=_MR1Dp8-F8w"
    )


    learning_guide = """
BEFORE YOU WATCH

You have already learned Work, Energy and Power
through the Rich Notes.

Now use the video to connect the formulas
with physical situations.


WHAT TO LOOK FOR

1. When is mechanical work actually done?

2. Why does displacement matter when calculating work?

3. What is kinetic energy?

4. What is gravitational potential energy?

5. How can energy change from one form to another?

6. What is the difference between work and power?

7. Why does completing the same work faster mean greater power?


WORK

Mechanical work is done when a force causes displacement.


For force acting in the same direction as motion:

W = F × s


Where:

W = Work

F = Force

s = Displacement


REAL-WORLD CONNECTION

Imagine pushing a box.

If the box moves:

Force + Displacement
→ Work is done.


If you push a rigid wall
and it does not move:

Displacement = 0

Therefore:

Work done on the wall = 0.


KINETIC ENERGY

A moving object possesses kinetic energy.


Formula:

KE = 1/2 × m × v²


Where:

m = mass

v = velocity


IMPORTANT CONNECTION

Velocity is squared.

So increasing speed can increase kinetic energy significantly.


REAL-WORLD EXAMPLE

A moving car contains kinetic energy.

When brakes are applied:

Kinetic Energy
→ Thermal Energy

through friction.


POTENTIAL ENERGY

An object can store energy because of its position.


Gravitational Potential Energy:

PE = m × g × h


Where:

m = mass

g = acceleration due to gravity

h = height


REAL-WORLD EXAMPLES

• Water stored behind a dam
• Book on a shelf
• Roller coaster at the top
• Lifted hammer
• Load raised by a crane


ENERGY TRANSFORMATION

Consider a ball falling from a height.


At the top:

More Potential Energy

Less Kinetic Energy


While falling:

Potential Energy decreases

Kinetic Energy increases


Near the bottom:

More Kinetic Energy


This demonstrates energy transformation.


CONSERVATION OF ENERGY

Energy does not simply disappear.

It can:

• Transfer between objects
• Change from one form to another


Examples:

Chemical Energy
→ Electrical Energy

Electrical Energy
→ Mechanical Energy

Potential Energy
→ Kinetic Energy

Kinetic Energy
→ Thermal Energy


POWER

Power tells us how quickly work is done.


Formula:

P = W / t


Where:

P = Power

W = Work

t = Time


SI Unit:

Watt


STAIRCASE EXAMPLE

Two people climb the same staircase.

Suppose they perform the same amount of work.


Person A takes:

10 seconds


Person B takes:

5 seconds


Person B performs the same work
in less time.

Therefore:

Person B has greater power.


SELF CHECK 1

A force of 20 N moves an object 5 m
in the same direction.

Work:

W = F × s

W = 20 × 5

W = 100 J


SELF CHECK 2

A 2 kg object moves at 4 m/s.

Kinetic Energy:

KE = 1/2 × 2 × 4²

KE = 16 J


SELF CHECK 3

A motor performs 600 J of work
in 3 seconds.

Power:

P = W / t

P = 600 / 3

P = 200 W


ENGINEERING CONNECTION

These concepts are used in:

• Motors
• Engines
• Electric vehicles
• Robotics
• Cranes
• Elevators
• Power plants
• Renewable energy systems
• Manufacturing machines


AFTER WATCHING

You should be able to explain:

WORK

Force causing displacement.


ENERGY

Ability to perform work or cause change.


KINETIC ENERGY

Energy due to motion.


POTENTIAL ENERGY

Stored energy due to position.


POWER

Rate at which work is done.


FINAL CONNECTION

Force + Displacement
→ Work

Motion
→ Kinetic Energy

Height
→ Potential Energy

Energy changing form
→ Conservation of Energy

Work / Time
→ Power


KEY TAKEAWAY

Work tells us how much energy is transferred.

Energy tells us the ability to cause change.

Power tells us how quickly that energy transfer happens.
"""


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
    print(" TOPIC 4 YOUTUBE VIDEO UPDATED")
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
    print("TOPIC 4 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()