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
    # TOPIC 5
    # =========================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == 5
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 5 not found."
        )


    # =========================================================
    # VIDEO DETAILS
    # =========================================================

    video_title = (
        "Momentum & Conservation of Linear Momentum"
    )


    video_description = (
        "A guided Physics lesson introducing momentum, "
        "mass and velocity, momentum direction, force, "
        "change in momentum and conservation of momentum."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=NIVNfI0RN2k"
    )


    learning_guide = """
BEFORE YOU WATCH

You already studied:

• Momentum
• Impulse
• Collisions
• Conservation of momentum

through the Rich Notes.

Now use this video to strengthen the connection
between mass, velocity, force and momentum.


WHAT TO LOOK FOR

1. What is momentum?

2. Why does momentum depend on both mass and velocity?

3. Why is momentum a vector quantity?

4. What happens to momentum when a force acts?

5. How are Newton's Laws connected with momentum?

6. Why is total momentum conserved during a collision?

7. Why must direction be considered in momentum problems?


MOMENTUM

Momentum describes the motion of an object
using both mass and velocity.


FORMULA

p = m × v


Where:

p = Momentum

m = Mass

v = Velocity


SI UNIT

kg·m/s


REAL-WORLD CONNECTION

Imagine:

A bicycle

and

A heavy truck

moving at the same velocity.


The truck has greater mass.

Therefore:

Truck mass ↑

→ Momentum ↑

→ More difficult to stop


This is why mass strongly affects
the motion and stopping behaviour of vehicles.


MOMENTUM AND VELOCITY

Momentum is a VECTOR quantity.

That means direction matters.


Example:

100 kg·m/s east

and

100 kg·m/s west

have equal magnitudes,

but their momentum vectors
point in opposite directions.


CONNECT WITH TOPIC 2

Speed tells:

How fast?


Velocity tells:

How fast + Direction


Because momentum uses velocity:

Momentum also has direction.


FORCE AND CHANGE IN MOMENTUM

A force can change an object's momentum.


If an object:

• Speeds up
• Slows down
• Changes direction

its velocity changes.

Therefore its momentum changes.


This connects momentum with Newton's Second Law.


IMPULSE CONNECTION

When a force acts for some period of time:

Impulse
=
Force × Time


J = F × Δt


Impulse is equal to
the change in momentum.


J = Δp


REAL-WORLD EXAMPLE — CATCHING A BALL

Imagine catching a fast cricket ball.


If you stop the ball almost instantly:

Stopping time is small.

The force can be large.


Instead, players move their hands backward
while catching the ball.

This increases the stopping time.


For the same change in momentum:

Longer stopping time
→ Smaller average force.


SAFETY CONNECTION

The same principle helps explain:

• Airbags
• Seat belts
• Helmets
• Crash cushions
• Sports padding


COLLISIONS

During a collision,
two objects exert forces on each other.

Because these forces act during the interaction,
the momentum of each object can change.


Example:

Moving ball hits stationary ball.

Before collision:

Ball A has momentum.

Ball B may have zero momentum.


During collision:

Momentum is transferred.


After collision:

Both objects may have different velocities.


CONSERVATION OF MOMENTUM

For an isolated system:

TOTAL MOMENTUM BEFORE
=
TOTAL MOMENTUM AFTER


For two objects:

m₁u₁ + m₂u₂

=

m₁v₁ + m₂v₂


Where:

u = initial velocity

v = final velocity


WHY IS MOMENTUM CONSERVED?

During the collision,
the objects exert forces on each other.

Newton's Third Law tells us
these interaction forces are equal and opposite.

Their momentum changes balance.

Therefore the total momentum
of the isolated system remains constant.


IMPORTANT CONDITION

Momentum conservation is applied to the system
when external forces are negligible
during the interaction.


COLLISION TYPES — CONNECT WITH NOTES

Our Rich Notes also introduced
different collision types.


ELASTIC COLLISION

Momentum conserved.

Kinetic energy also conserved.


INELASTIC COLLISION

Momentum conserved.

Some kinetic energy changes into:

• Heat
• Sound
• Deformation
• Internal energy


PERFECTLY INELASTIC COLLISION

The objects stick together after collision
and move with a common velocity.


IMPORTANT

Do not confuse:

Conservation of Momentum

with

Conservation of Kinetic Energy.


Momentum can remain conserved
even when mechanical kinetic energy changes form.


SELF CHECK 1

Mass = 4 kg

Velocity = 6 m/s


Momentum:

p = m × v

p = 4 × 6

p = 24 kg·m/s


SELF CHECK 2

A moving object doubles its velocity
while mass remains constant.

Since:

p = mv

its momentum also doubles.


SELF CHECK 3

During an isolated collision:

Total momentum before
=
Total momentum after.


REAL-WORLD APPLICATIONS

Momentum and collision analysis are used in:

• Vehicle crash safety
• Airbags
• Seat belts
• Sports
• Robotics
• Railway systems
• Industrial machines
• Spacecraft
• Rocket propulsion
• Collision detection and control


ENGINEERING CONNECTION

Suppose a robot arm catches
or stops a moving object.

The controller must understand:

• Object mass
• Object velocity
• Momentum
• Stopping time
• Impact force

Increasing the stopping time can help
reduce damaging impact forces.


AFTER WATCHING

You should be able to explain:


MOMENTUM

Mass × Velocity


IMPULSE

Force × Time


IMPULSE-MOMENTUM CONNECTION

Impulse
=
Change in Momentum


COLLISION

Interaction between moving objects
that changes their momenta.


CONSERVATION OF MOMENTUM

Total momentum of an isolated system
remains constant.


FINAL CONNECTION

Mass + Velocity
→ Momentum


Force acting over time
→ Impulse


Impulse
→ Momentum changes


Objects collide
→ Momentum transfers


Isolated system
→ Total momentum remains conserved


KEY TAKEAWAY

Momentum may move from one object to another,
but in an isolated system the total amount
of momentum remains unchanged.
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
    print(" TOPIC 5 YOUTUBE VIDEO UPDATED")
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
    print("TOPIC 5 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()