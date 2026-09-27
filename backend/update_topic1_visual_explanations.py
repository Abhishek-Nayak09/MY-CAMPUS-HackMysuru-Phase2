from app.db.database import SessionLocal

from app.models.user import User
from app.models.topic import Topic
from app.models.note import Note, NoteSection


db = SessionLocal()


try:

    # =========================================================
    # FIND TOPIC + NOTE
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
        raise Exception("Topic not found")


    note = (
        db.query(Note)
        .filter(
            Note.topic_id == topic.id,
            Note.is_active == True
        )
        .first()
    )


    if not note:
        raise Exception("Rich note not found")


    # =========================================================
    # SECTION 1 — MORNING PHYSICS
    # =========================================================

    morning = (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id,
            NoteSection.section_order == 1
        )
        .first()
    )


    morning.body = """
WHAT IS HAPPENING IN THIS SCENE?

Your normal morning already contains several Physics concepts.


1. PHONE ALARM → SOUND WAVES

Inside your phone, the speaker vibrates.

Those vibrations disturb nearby air particles.

The disturbance travels through the air as a sound wave
until it reaches your ears.

PHYSICS CONNECTION:
Vibration → Sound Wave → Hearing

KEY IDEA:
Sound needs vibrations to transfer energy through a medium.


2. WALKING → FRICTION

When you walk, your foot pushes backward against the ground.

The ground provides friction in the opposite direction,
helping your body move forward.

Without enough friction, your foot would simply slip.

PHYSICS CONNECTION:
Foot pushes ground backward
→ Ground pushes foot forward
→ You move forward

KEY IDEA:
Friction is essential for walking.


3. MOVING CAR → FORCE AND MOTION

The engine produces force.

Through the tyres, that force interacts with the road.

The car accelerates when there is a net forward force.

When brakes are applied, forces oppose the motion
and the vehicle slows down.

PHYSICS CONNECTION:
Force → Acceleration → Motion

KEY IDEA:
A change in motion requires force.


4. SUNLIGHT → LIGHT AND ENERGY

The Sun transfers energy to Earth through electromagnetic radiation.

Visible light is one part of that radiation.

That energy provides daylight and also warms objects.

PHYSICS CONNECTION:
Sun → Electromagnetic Radiation → Energy Transfer

KEY IDEA:
Light can carry energy through space.


WHY THIS MATTERS

Before reaching your classroom,
you have already experienced:

• Waves
• Friction
• Force
• Motion
• Energy
• Light

That is why Physics is not separate from everyday life.
Physics explains the everyday life itself.
"""


    morning.caption = (
        "Your morning connects sound waves, friction, force, motion "
        "and light energy before your first class even begins."
    )


    # =========================================================
    # SECTION 3 — FOOTBALL
    # =========================================================

    football = (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id,
            NoteSection.section_order == 3
        )
        .first()
    )


    football.body = """
WHAT HAPPENS WHEN YOU KICK THE BALL?

Initially, the football is at rest.

When your foot touches the ball,
your foot applies a contact FORCE.

That force changes the motion of the ball
and gives it an initial velocity.


STEP 1 — THE KICK

Your foot pushes the football.

PHYSICS:
Force causes a change in motion.

This connects to Newton's Laws of Motion.


STEP 2 — THE BALL MOVES FORWARD

After leaving your foot,
the ball already has forward velocity.

It does not need your foot to continuously push it.

PHYSICS:
Because of inertia, the ball tends to continue moving.


STEP 3 — GRAVITY PULLS DOWNWARD

While the ball moves forward,
Earth's gravity continuously accelerates it downward.

So two things happen together:

Forward motion
+
Downward gravitational acceleration


STEP 4 — A CURVED PATH APPEARS

Because the ball continues moving forward
while gravity pulls it downward,
its path becomes curved.

That curved motion is called projectile motion.


PHYSICS CONNECTION

Kick
→ Force
→ Initial Velocity
→ Inertia
→ Gravity
→ Curved Trajectory


REAL-WORLD CONNECTION

The same idea is used to understand:

• Football kicks
• Basketball shots
• Cricket balls
• Javelin throws
• Water fountains
• Projectile motion


ONE-LINE TAKEAWAY

The football follows a curved path because it keeps moving
forward while gravity continuously pulls it downward.
"""


    football.caption = (
        "The kick provides the initial motion; gravity continuously "
        "pulls the football downward, creating its curved trajectory."
    )


    # =========================================================
    # SECTION 5 — ROCKET
    # =========================================================

    rocket = (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id,
            NoteSection.section_order == 5
        )
        .first()
    )


    rocket.body = """
WHY DOES THE ROCKET MOVE UP?

A rocket engine burns fuel.

Combustion produces extremely hot,
high-pressure gases inside the engine.

The engine directs these gases downward
through the rocket nozzle at very high speed.


STEP 1 — FUEL BURNS

Chemical energy stored in the fuel
is released during combustion.

This produces hot expanding gases.


STEP 2 — GAS IS PUSHED DOWNWARD

The rocket engine forces those gases
out through the nozzle.

ACTION:

Rocket pushes exhaust gases DOWNWARD.


STEP 3 — THE ROCKET IS PUSHED UPWARD

The exhaust gases exert an equal force
in the opposite direction on the rocket.

REACTION:

Exhaust gases push the rocket UPWARD.


THIS IS NEWTON'S THIRD LAW

For every action,
there is an equal and opposite reaction.


PHYSICS CONNECTION

Fuel burns
→ Hot gas forms
→ Gas accelerates downward
→ Opposite force acts upward
→ Rocket gains thrust


WHAT IS THRUST?

The upward force produced by the rocket engine
is called THRUST.

If the upward thrust becomes greater than
the downward effects acting on the rocket,
the rocket accelerates upward.


IMPORTANT IDEA

A rocket does NOT need to push against air.

The rocket works because it throws mass
— exhaust gases —
backward/downward at high speed.

That is why rockets can also operate in space.


REAL-WORLD CONNECTION

This principle is used in:

• Launch vehicles
• Satellites
• Spacecraft
• Jet propulsion concepts
• Maneuvering thrusters


ONE-LINE TAKEAWAY

🔥 Fuel burns
→ gases are expelled DOWN
→ gases push the rocket UP
→ the rocket produces THRUST.

This is Newton's Third Law of Motion.
"""


    rocket.caption = (
        "The engine accelerates exhaust gases downward. "
        "The equal and opposite reaction produces upward thrust on the rocket."
    )


    # =========================================================
    # SAVE
    # =========================================================

    db.commit()


    print("")
    print("==========================================")
    print(" VISUAL EXPLANATIONS UPDATED SUCCESSFULLY")
    print("==========================================")
    print("")
    print("Morning Physics  : UPDATED")
    print("Football Physics : UPDATED")
    print("Rocket Physics   : UPDATED")
    print("")


except Exception as error:

    db.rollback()

    print("")
    print("UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()