import json
from pathlib import Path

from app.db.database import SessionLocal

from app.models.user import User
from app.models.course import Course
from app.models.year import AcademicYear
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic
from app.models.note import Note, NoteSection


# =========================================================
# PATHS
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parent

MEDIA_DIR = (
    BACKEND_DIR
    / "uploads"
    / "notes"
    / "physics"
    / "topic_5"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — MOMENTUM
# =========================================================

momentum_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430">

    <rect
        width="1000"
        height="430"
        rx="28"
        fill="#eef2ff"
    />

    <text
        x="45"
        y="60"
        font-family="Arial"
        font-size="32"
        font-weight="700"
        fill="#172033"
    >
        Momentum Depends on Mass and Velocity
    </text>

    <!-- SMALL CAR -->

    <g>

        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0;220 0;0 0"
            dur="4s"
            repeatCount="indefinite"
        />

        <rect
            x="100"
            y="170"
            width="170"
            height="65"
            rx="20"
            fill="#2563eb"
        />

        <circle
            cx="140"
            cy="240"
            r="22"
            fill="#111827"
        />

        <circle
            cx="230"
            cy="240"
            r="22"
            fill="#111827"
        />

    </g>

    <text
        x="100"
        y="300"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Lower mass
    </text>

    <!-- TRUCK -->

    <g>

        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0;120 0;0 0"
            dur="4s"
            repeatCount="indefinite"
        />

        <rect
            x="570"
            y="150"
            width="250"
            height="90"
            rx="20"
            fill="#7c3aed"
        />

        <rect
            x="760"
            y="120"
            width="90"
            height="120"
            rx="15"
            fill="#6d28d9"
        />

        <circle
            cx="625"
            cy="250"
            r="27"
            fill="#111827"
        />

        <circle
            cx="780"
            cy="250"
            r="27"
            fill="#111827"
        />

    </g>

    <text
        x="620"
        y="305"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Greater mass
    </text>

    <text
        x="320"
        y="380"
        font-family="Arial"
        font-size="25"
        font-weight="700"
        fill="#4338ca"
    >
        Momentum: p = m × v
    </text>

</svg>
"""


# =========================================================
# SVG 2 — COLLISION
# =========================================================

collision_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430">

    <rect
        width="1000"
        height="430"
        rx="28"
        fill="#fff7ed"
    />

    <text
        x="45"
        y="60"
        font-family="Arial"
        font-size="32"
        font-weight="700"
        fill="#172033"
    >
        Collision — Momentum Transfers Between Objects
    </text>

    <!-- BALL 1 -->

    <circle
        cx="250"
        cy="235"
        r="50"
        fill="#2563eb"
    >

        <animate
            attributeName="cx"
            values="250;450;450"
            dur="3s"
            repeatCount="indefinite"
        />

    </circle>

    <!-- BALL 2 -->

    <circle
        cx="580"
        cy="235"
        r="50"
        fill="#ef4444"
    >

        <animate
            attributeName="cx"
            values="580;580;760"
            dur="3s"
            repeatCount="indefinite"
        />

    </circle>

    <!-- ARROW -->

    <line
        x1="120"
        y1="140"
        x2="330"
        y2="140"
        stroke="#16a34a"
        stroke-width="8"
    />

    <polygon
        points="350,140 315,120 315,160"
        fill="#16a34a"
    />

    <text
        x="140"
        y="115"
        font-family="Arial"
        font-size="20"
        fill="#15803d"
    >
        Initial motion
    </text>

    <text
        x="230"
        y="365"
        font-family="Arial"
        font-size="21"
        fill="#172033"
    >
        Before collision
    </text>

    <text
        x="625"
        y="365"
        font-family="Arial"
        font-size="21"
        fill="#172033"
    >
        After collision
    </text>

</svg>
"""


# =========================================================
# SVG 3 — CONSERVATION OF MOMENTUM
# =========================================================

conservation_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430">

    <rect
        width="1000"
        height="430"
        rx="28"
        fill="#ecfdf5"
    />

    <text
        x="45"
        y="60"
        font-family="Arial"
        font-size="32"
        font-weight="700"
        fill="#172033"
    >
        Conservation of Momentum
    </text>

    <rect
        x="80"
        y="115"
        width="360"
        height="220"
        rx="20"
        fill="#ffffff"
        stroke="#bbf7d0"
        stroke-width="3"
    />

    <text
        x="125"
        y="160"
        font-family="Arial"
        font-size="24"
        font-weight="700"
        fill="#166534"
    >
        Before Collision
    </text>

    <text
        x="120"
        y="225"
        font-family="Arial"
        font-size="22"
        fill="#172033"
    >
        Total Momentum = P
    </text>

    <rect
        x="560"
        y="115"
        width="360"
        height="220"
        rx="20"
        fill="#ffffff"
        stroke="#bbf7d0"
        stroke-width="3"
    />

    <text
        x="620"
        y="160"
        font-family="Arial"
        font-size="24"
        font-weight="700"
        fill="#166534"
    >
        After Collision
    </text>

    <text
        x="610"
        y="225"
        font-family="Arial"
        font-size="22"
        fill="#172033"
    >
        Total Momentum = P
    </text>

    <text
        x="415"
        y="230"
        font-family="Arial"
        font-size="42"
        font-weight="700"
        fill="#4f46e5"
    >
        =
    </text>

    <text
        x="260"
        y="390"
        font-family="Arial"
        font-size="24"
        font-weight="700"
        fill="#15803d"
    >
        Total momentum remains constant in an isolated system
    </text>

</svg>
"""


# =========================================================
# SAVE VISUALS
# =========================================================

(
    MEDIA_DIR
    / "momentum_mass_velocity.svg"
).write_text(
    momentum_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "collision_transfer.svg"
).write_text(
    collision_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "momentum_conservation.svg"
).write_text(
    conservation_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # TOPIC 5
    # =====================================================

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


    # =====================================================
    # CREATE / UPDATE NOTE
    # =====================================================

    note = (
        db.query(Note)
        .filter(
            Note.topic_id == topic.id,
            Note.is_active == True
        )
        .first()
    )


    if not note:

        note = Note(

            topic_id=
                topic.id,

            created_by=
                None,

            title=
                "Momentum & Collisions",

            subtitle=
                "Understand how mass and velocity affect motion and what happens when objects collide.",

            introduction=
                "A moving football, a speeding car and a heavy truck all carry momentum. When objects collide, momentum can transfer between them—but the total momentum of an isolated system remains conserved.",

            pdf_url=
                None,

            version=
                1,

            is_active=
                True
        )


        db.add(note)

        db.commit()

        db.refresh(note)


    else:

        note.title = (
            "Momentum & Collisions"
        )

        note.subtitle = (
            "Understand how mass and velocity affect motion and what happens when objects collide."
        )

        note.introduction = (
            "A moving football, a speeding car and a heavy truck all carry momentum. When objects collide, momentum can transfer between them—but the total momentum of an isolated system remains conserved."
        )

        db.commit()


    # =====================================================
    # DELETE OLD SECTIONS
    # =====================================================

    (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id
        )
        .delete(
            synchronize_session=False
        )
    )


    # =====================================================
    # CONTENT
    # =====================================================

    sections = [

        # -------------------------------------------------
        # MOMENTUM STORY
        # -------------------------------------------------

        {
            "order": 10,

            "type": "story",

            "heading":
                "Why Is a Moving Truck Harder to Stop Than a Bicycle?",

            "body": """
Imagine two vehicles moving at the same speed:

A bicycle

and

A heavy truck.


Both are moving.

But stopping the truck requires much more effort.

Why?

Because the truck has much greater mass.

A moving object's resistance to being stopped
is related to a quantity called MOMENTUM.


MOMENTUM

Momentum is the product of:

Mass
and
Velocity.


FORMULA

p = m × v


Where:

p = Momentum

m = Mass

v = Velocity


SI UNIT

kg·m/s


IMPORTANT

Momentum depends on BOTH:

• Mass
• Velocity


So:

Greater mass
→ Greater momentum

Greater velocity
→ Greater momentum


ONE-LINE TAKEAWAY

Momentum tells us how difficult it is
to stop or change the motion of a moving object.
""",

            "media_url":
                "/uploads/notes/physics/topic_5/momentum_mass_velocity.svg",

            "media_type":
                "svg",

            "caption":
                "For the same velocity, an object with greater mass has greater momentum.",

            "alt_text":
                "Animated car and truck illustrating the effect of mass on momentum."
        },


        # -------------------------------------------------
        # CHECKPOINT 1
        # -------------------------------------------------

        {
            "order": 15,

            "type": "checkpoint",

            "heading":
                "Quick Check 1 — Calculate Momentum",

            "body":
                "Use p = m × v.",

            "interactive": {

                "question":
                    "A 4 kg object moves at 6 m/s. What is its momentum?",

                "options": [
                    "10 kg·m/s",
                    "24 kg·m/s",
                    "2 kg·m/s",
                    "36 kg·m/s"
                ],

                "answer":
                    "24 kg·m/s",

                "explanation":
                    "Momentum p = m × v = 4 × 6 = 24 kg·m/s."
            }
        },


        # -------------------------------------------------
        # DIRECTION
        # -------------------------------------------------

        {
            "order": 20,

            "type": "definition",

            "heading":
                "Momentum Has Direction",

            "body": """
Momentum is a VECTOR quantity.

That means it has:

• Magnitude
• Direction


Because:

p = m × v

and velocity has direction.


EXAMPLE

Car A:

Mass = 1000 kg

Velocity = 10 m/s east


Momentum:

p = 1000 × 10

= 10,000 kg·m/s east


Car B:

Same mass

Same speed

but moving west.


Its momentum points west.


IMPORTANT

Two objects can have the same momentum magnitude
but different momentum directions.


ONE-LINE TAKEAWAY

Momentum always points in the same direction
as the object's velocity.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # IMPULSE
        # -------------------------------------------------

        {
            "order": 30,

            "type": "real_world",

            "heading":
                "Impulse — Changing Momentum",

            "body": """
To change an object's momentum,
a force must act over some amount of time.

This idea is called IMPULSE.


IMPULSE

Impulse = Force × Time


J = F × Δt


Impulse is equal to the change in momentum.


J = Δp


This means:

Force × Time
=
Change in Momentum


REAL-WORLD EXAMPLE — CATCHING A BALL

Imagine catching a fast cricket ball.

If you stop it instantly,
the stopping time is very small.

That can produce a large force.


But players often move their hands backward
while catching.

This increases the stopping time.

For the same change in momentum:

Longer stopping time
→ Smaller average force.


SAFETY CONNECTION

The same principle is used in:

• Airbags
• Seat belts
• Helmets
• Crash cushions
• Sports padding


These devices increase the time
over which momentum changes.

This reduces the force experienced.


ONE-LINE TAKEAWAY

Increasing stopping time can reduce impact force.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # CHECKPOINT 2
        # -------------------------------------------------

        {
            "order": 35,

            "type": "checkpoint",

            "heading":
                "Quick Check 2 — Why Do Airbags Help?",

            "body":
                "Connect impulse with safety.",

            "interactive": {

                "question":
                    "Why can an airbag reduce the force experienced by a passenger during a collision?",

                "options": [
                    "It increases the time over which momentum changes",
                    "It increases the passenger's momentum",
                    "It removes the passenger's mass",
                    "It increases vehicle speed"
                ],

                "answer":
                    "It increases the time over which momentum changes",

                "explanation":
                    "For the same change in momentum, increasing the stopping time reduces the average force. Airbags help increase this stopping time."
            }
        },


        # -------------------------------------------------
        # COLLISIONS
        # -------------------------------------------------

        {
            "order": 40,

            "type": "animation",

            "heading":
                "What Happens During a Collision?",

            "body": """
A collision occurs when two objects interact
for a short period of time
and exert large forces on each other.


Examples:

• Two cars colliding
• Billiard balls hitting each other
• Football hitting a player's foot
• Two carts colliding
• A hammer striking a nail


During a collision:

One object's momentum can change.

The other object's momentum also changes.


Because of Newton's Third Law:

Each object exerts an equal and opposite force
on the other.


These interaction forces act for the same time interval.


Therefore momentum is transferred
between the objects.


IMPORTANT

Momentum is not simply “lost.”

In an isolated system,
the TOTAL momentum remains constant.


ONE-LINE TAKEAWAY

During a collision, momentum can transfer
from one object to another.
""",

            "media_url":
                "/uploads/notes/physics/topic_5/collision_transfer.svg",

            "media_type":
                "svg",

            "caption":
                "During a collision, momentum can transfer between interacting objects.",

            "alt_text":
                "Animated collision between two objects showing momentum transfer."
        },


        # -------------------------------------------------
        # CONSERVATION
        # -------------------------------------------------

        {
            "order": 50,

            "type": "application",

            "heading":
                "Law of Conservation of Momentum",

            "body": """
One of the most important laws in collision problems is:

THE LAW OF CONSERVATION OF MOMENTUM.


For an isolated system:

Total momentum before collision
=
Total momentum after collision.


In symbolic form:

Σp before
=
Σp after


FOR TWO OBJECTS

Before collision:

m₁u₁ + m₂u₂


After collision:

m₁v₁ + m₂v₂


Therefore:

m₁u₁ + m₂u₂
=
m₁v₁ + m₂v₂


Where:

u = initial velocity

v = final velocity


WHY IS MOMENTUM CONSERVED?

During the collision,
the forces between the objects are internal forces.

By Newton's Third Law,
these interaction forces are equal and opposite.

The momentum changes of the two objects
balance each other.

So total momentum stays constant
if external forces are negligible.


ONE-LINE TAKEAWAY

Momentum may move between objects,
but total momentum of an isolated system stays constant.
""",

            "media_url":
                "/uploads/notes/physics/topic_5/momentum_conservation.svg",

            "media_type":
                "svg",

            "caption":
                "In an isolated system, total momentum before a collision equals total momentum after it.",

            "alt_text":
                "Diagram showing equal total momentum before and after a collision."
        },


        # -------------------------------------------------
        # CHECKPOINT 3
        # -------------------------------------------------

        {
            "order": 55,

            "type": "checkpoint",

            "heading":
                "Quick Check 3 — Conservation of Momentum",

            "body":
                "Think about the whole isolated system.",

            "interactive": {

                "question":
                    "In an isolated collision system with negligible external forces, what happens to the total momentum?",

                "options": [
                    "It is conserved",
                    "It always becomes zero",
                    "It always increases",
                    "It disappears after impact"
                ],

                "answer":
                    "It is conserved",

                "explanation":
                    "The total momentum before and after the collision remains equal when external forces are negligible."
            }
        },


        # -------------------------------------------------
        # COLLISION TYPES
        # -------------------------------------------------

        {
            "order": 60,

            "type": "definition",

            "heading":
                "Elastic and Inelastic Collisions",

            "body": """
Not all collisions behave the same way.


ELASTIC COLLISION

In an ideal elastic collision:

• Momentum is conserved
• Kinetic energy is also conserved


A useful approximation can be seen
with hard objects such as:

• Billiard balls
• Some molecular collisions


INELASTIC COLLISION

Momentum is conserved,
but kinetic energy is not fully conserved
as mechanical kinetic energy.


Some kinetic energy may become:

• Heat
• Sound
• Deformation
• Internal energy


PERFECTLY INELASTIC COLLISION

The objects stick together
after the collision.

They then move with a common velocity.


EXAMPLE

Two clay balls collide
and stick together.

This is approximately
a perfectly inelastic collision.


IMPORTANT

Even when kinetic energy changes form:

Momentum can still be conserved.


ONE-LINE TAKEAWAY

Momentum conservation applies to isolated collisions,
but kinetic energy behavior depends on collision type.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # CHECKPOINT 4
        # -------------------------------------------------

        {
            "order": 65,

            "type": "checkpoint",

            "heading":
                "Quick Check 4 — Collision Type",

            "body":
                "Identify the collision from what happens afterward.",

            "interactive": {

                "question":
                    "Two objects collide and stick together after impact. What type of collision is this?",

                "options": [
                    "Perfectly inelastic collision",
                    "Perfectly elastic collision",
                    "No collision",
                    "Uniform motion"
                ],

                "answer":
                    "Perfectly inelastic collision",

                "explanation":
                    "When the colliding objects stick together and move as one body after impact, the collision is called perfectly inelastic."
            }
        },


        # -------------------------------------------------
        # APPLICATIONS
        # -------------------------------------------------

        {
            "order": 70,

            "type": "application",

            "heading":
                "Where Are Momentum and Collisions Used?",

            "body": """
🚗 VEHICLE SAFETY

Engineers study momentum and impulse
when designing:

• Airbags
• Seat belts
• Crumple zones
• Crash barriers


🏏 SPORTS

Momentum affects:

• Cricket balls
• Football tackles
• Bat-ball collisions
• Racquet sports


🚀 ROCKETS

A rocket ejects gases backward.

Momentum conservation helps explain
the rocket's forward motion.


🔫 RECOIL PRINCIPLE

When an object is launched forward,
another part of the system can experience
momentum in the opposite direction.


🤖 ROBOTICS

Robots interacting with moving objects
must account for:

• Momentum
• Impact force
• Collision safety


🚂 TRANSPORT

Collision analysis helps engineers understand
how vehicles behave during impacts.


🏭 INDUSTRIAL MACHINES

Momentum and impact analysis are important
in presses, hammers and moving machinery.


These ideas are essential
for safety, motion control and mechanical design.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        {
            "order": 80,

            "type": "summary",

            "heading":
                "What Should You Remember?",

            "body": """
MOMENTUM

p = m × v

Depends on mass and velocity.

Momentum is a vector quantity.


IMPULSE

J = F × Δt

Impulse equals change in momentum.


COLLISION

A short interaction where objects exert
large forces on each other.


CONSERVATION OF MOMENTUM

For an isolated system:

Total momentum before
=
Total momentum after.


ELASTIC COLLISION

Momentum conserved.

Kinetic energy conserved.


INELASTIC COLLISION

Momentum conserved.

Some kinetic energy changes into other forms.


PERFECTLY INELASTIC COLLISION

Objects stick together after impact.


FINAL CONNECTION

Mass + Velocity
→ Momentum

Force acting over time
→ Impulse

Impulse
→ Change in Momentum

Collision
→ Momentum Transfer

Isolated System
→ Total Momentum Conserved


Momentum gives us a powerful way
to understand impacts, collisions,
vehicle safety and moving systems.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        }

    ]


    # =====================================================
    # INSERT
    # =====================================================

    for item in sections:

        interactive_data = None


        if item.get("interactive"):

            interactive_data = json.dumps(
                item["interactive"]
            )


        section = NoteSection(

            note_id=
                note.id,

            section_order=
                item["order"],

            section_type=
                item["type"],

            heading=
                item["heading"],

            body=
                item.get("body"),

            media_url=
                item.get("media_url"),

            media_type=
                item.get("media_type"),

            caption=
                item.get("caption"),

            alt_text=
                item.get("alt_text"),

            interactive_data=
                interactive_data,

            is_active=
                True
        )


        db.add(section)


    db.commit()


    # =====================================================
    # VERIFY
    # =====================================================

    saved_sections = (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id
        )
        .order_by(
            NoteSection.section_order
        )
        .all()
    )


    checkpoint_count = sum(
        1
        for section in saved_sections
        if section.section_type == "checkpoint"
    )


    print("")
    print("==========================================")
    print(" TOPIC 5 RICH NOTES CREATED SUCCESSFULLY")
    print("==========================================")
    print("")

    print(
        f"Topic ID : {topic.id}"
    )

    print(
        f"Topic    : {topic.title}"
    )

    print(
        f"Note ID  : {note.id}"
    )

    print(
        f"Sections : {len(saved_sections)}"
    )

    print("")


    for section in saved_sections:

        print(
            f"{section.section_order}. "
            f"{section.section_type.upper()} "
            f"- {section.heading}"
        )


    print("")

    print(
        f"Total checkpoints: {checkpoint_count}"
    )

    print("")

    print("Generated visuals:")

    print(
        MEDIA_DIR
        / "momentum_mass_velocity.svg"
    )

    print(
        MEDIA_DIR
        / "collision_transfer.svg"
    )

    print(
        MEDIA_DIR
        / "momentum_conservation.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 5 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()