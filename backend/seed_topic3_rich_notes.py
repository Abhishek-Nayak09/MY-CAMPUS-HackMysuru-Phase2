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
# MEDIA PATH
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parent

MEDIA_DIR = (
    BACKEND_DIR
    / "uploads"
    / "notes"
    / "physics"
    / "topic_3"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — FORCE CHANGES MOTION
# =========================================================

force_motion_svg = """
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
        Force Can Change Motion
    </text>

    <!-- BOX -->

    <g id="box">

        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0;360 0;0 0"
            dur="5s"
            repeatCount="indefinite"
        />

        <rect
            x="180"
            y="230"
            width="130"
            height="100"
            rx="12"
            fill="#6366f1"
        />

        <text
            x="245"
            y="290"
            font-family="Arial"
            font-size="22"
            text-anchor="middle"
            fill="white"
        >
            BOX
        </text>

    </g>

    <!-- FORCE ARROW -->

    <line
        x1="80"
        y1="280"
        x2="160"
        y2="280"
        stroke="#dc2626"
        stroke-width="10"
    />

    <polygon
        points="175,280 145,260 145,300"
        fill="#dc2626"
    />

    <text
        x="80"
        y="245"
        font-family="Arial"
        font-size="22"
        fill="#dc2626"
    >
        PUSH
    </text>

    <!-- ROAD -->

    <line
        x1="80"
        y1="335"
        x2="900"
        y2="335"
        stroke="#64748b"
        stroke-width="8"
    />

    <text
        x="350"
        y="390"
        font-family="Arial"
        font-size="22"
        fill="#172033"
    >
        Net Force → Acceleration → Change in Motion
    </text>

</svg>
"""


# =========================================================
# SVG 2 — NEWTON FIRST LAW / INERTIA
# =========================================================

inertia_svg = """
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
        Newton's First Law — Inertia
    </text>

    <!-- CAR -->

    <rect
        x="150"
        y="230"
        width="280"
        height="85"
        rx="25"
        fill="#2563eb"
    />

    <circle
        cx="205"
        cy="320"
        r="28"
        fill="#111827"
    />

    <circle
        cx="370"
        cy="320"
        r="28"
        fill="#111827"
    />

    <!-- PASSENGER -->

    <circle
        cx="290"
        cy="185"
        r="28"
        fill="#f59e0b"
    />

    <line
        x1="290"
        y1="213"
        x2="290"
        y2="265"
        stroke="#172033"
        stroke-width="10"
    />

    <!-- FORWARD BODY ARROW -->

    <line
        x1="300"
        y1="150"
        x2="520"
        y2="150"
        stroke="#ef4444"
        stroke-width="9"
    />

    <polygon
        points="540,150 505,130 505,170"
        fill="#ef4444"
    />

    <text
        x="350"
        y="125"
        font-family="Arial"
        font-size="20"
        fill="#ef4444"
    >
        Body tends to keep moving
    </text>

    <!-- BRAKE -->

    <text
        x="600"
        y="230"
        font-family="Arial"
        font-size="25"
        font-weight="700"
        fill="#172033"
    >
        CAR BRAKES
    </text>

    <text
        x="600"
        y="275"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Car stops quickly
    </text>

    <text
        x="600"
        y="310"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Passenger tends to continue forward
    </text>

    <text
        x="600"
        y="350"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#ea580c"
    >
        This is INERTIA
    </text>

</svg>
"""


# =========================================================
# SVG 3 — NEWTON THIRD LAW
# =========================================================

action_reaction_svg = """
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
        Newton's Third Law — Action &amp; Reaction
    </text>

    <!-- PERSON -->

    <circle
        cx="300"
        cy="160"
        r="34"
        fill="#f59e0b"
    />

    <line
        x1="300"
        y1="195"
        x2="300"
        y2="280"
        stroke="#172033"
        stroke-width="12"
    />

    <line
        x1="300"
        y1="225"
        x2="365"
        y2="250"
        stroke="#172033"
        stroke-width="10"
    />

    <line
        x1="300"
        y1="280"
        x2="260"
        y2="335"
        stroke="#172033"
        stroke-width="10"
    />

    <line
        x1="300"
        y1="280"
        x2="345"
        y2="335"
        stroke="#172033"
        stroke-width="10"
    />

    <!-- WALL -->

    <rect
        x="620"
        y="110"
        width="80"
        height="260"
        fill="#64748b"
    />

    <!-- ACTION -->

    <line
        x1="390"
        y1="245"
        x2="590"
        y2="245"
        stroke="#dc2626"
        stroke-width="10"
    />

    <polygon
        points="610,245 575,225 575,265"
        fill="#dc2626"
    />

    <text
        x="425"
        y="215"
        font-family="Arial"
        font-size="20"
        fill="#dc2626"
    >
        Action: Person pushes wall
    </text>

    <!-- REACTION -->

    <line
        x1="610"
        y1="300"
        x2="410"
        y2="300"
        stroke="#2563eb"
        stroke-width="10"
    />

    <polygon
        points="390,300 425,280 425,320"
        fill="#2563eb"
    />

    <text
        x="410"
        y="345"
        font-family="Arial"
        font-size="20"
        fill="#2563eb"
    >
        Reaction: Wall pushes person
    </text>

</svg>
"""


# =========================================================
# SAVE SVG
# =========================================================

(
    MEDIA_DIR
    / "force_changes_motion.svg"
).write_text(
    force_motion_svg,
    encoding="utf-8"
)


(
    MEDIA_DIR
    / "newton_first_law_inertia.svg"
).write_text(
    inertia_svg,
    encoding="utf-8"
)


(
    MEDIA_DIR
    / "newton_third_law.svg"
).write_text(
    action_reaction_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # FIND TOPIC 3
    # =====================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.title ==
            "Forces & Newton's Laws"
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 3 not found."
        )


    # =====================================================
    # NOTE
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

            topic_id=topic.id,

            created_by=None,

            title=
                "Forces & Newton's Laws",

            subtitle=
                "Understand why objects start, stop, accelerate and interact.",

            introduction=
                "Every push, pull, brake, jump and collision involves forces. Newton's Laws explain how those forces control motion.",

            pdf_url=None,

            version=1,

            is_active=True
        )


        db.add(note)

        db.commit()

        db.refresh(note)


    else:

        note.title = (
            "Forces & Newton's Laws"
        )

        note.subtitle = (
            "Understand why objects start, stop, accelerate and interact."
        )

        note.introduction = (
            "Every push, pull, brake, jump and collision involves forces. Newton's Laws explain how those forces control motion."
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
    # SECTIONS
    # =====================================================

    sections = [

        # -------------------------------------------------
        # FORCE
        # -------------------------------------------------

        {
            "order": 10,

            "type": "story",

            "heading":
                "What Is a Force?",

            "body": """
Imagine a football lying on the ground.

It remains there until someone kicks it.

The kick changes the motion of the football.

That interaction is called a FORCE.


FORCE

A force is a push or pull that can change
the state of motion of an object.


A FORCE CAN:

• Start a stationary object moving
• Stop a moving object
• Increase speed
• Decrease speed
• Change direction
• Change shape


SI UNIT

Newton

Symbol:

N


REAL-WORLD EXAMPLES

Opening a door → Push

Pulling a drawer → Pull

Kicking a football → Force changes motion

Braking a bike → Force reduces motion

Stretching a spring → Force changes shape


ONE-LINE TAKEAWAY

Force is a push or pull capable of changing motion.
""",

            "media_url":
                "/uploads/notes/physics/topic_3/force_changes_motion.svg",

            "media_type":
                "svg",

            "caption":
                "A net force can cause acceleration and change an object's motion.",

            "alt_text":
                "Animated box moving because of an applied force."
        },


        # -------------------------------------------------
        # BALANCED / UNBALANCED
        # -------------------------------------------------

        {
            "order": 20,

            "type": "definition",

            "heading":
                "Balanced and Unbalanced Forces",

            "body": """
Sometimes several forces act on the same object.


BALANCED FORCES

When forces are equal and opposite,
the net force becomes zero.

Net Force = 0


Example:

A book resting on a table.

Gravity pulls the book downward.

The table pushes the book upward.

These forces balance each other.

The book does not accelerate.


UNBALANCED FORCES

If the forces do not cancel,
there is a net force.

Net Force ≠ 0

The object accelerates.


Example:

You push a shopping cart forward.

If your forward push is greater than opposing forces,
the cart accelerates forward.


IMPORTANT

A net force does not simply mean
“the object is moving.”

It means:

“The object's velocity is changing.”


ONE-LINE TAKEAWAY

Balanced forces → no acceleration.

Unbalanced forces → acceleration.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # CHECK 1
        # -------------------------------------------------

        {
            "order": 25,

            "type": "checkpoint",

            "heading":
                "Quick Check 1 — Balanced Forces",

            "body":
                "Check your understanding of net force.",

            "interactive": {

                "question":
                    "A book is resting on a table. Gravity pulls downward and the table pushes upward with equal force. What is the net force?",

                "options": [
                    "Zero",
                    "Equal to gravity only",
                    "Double the gravitational force",
                    "Impossible to determine"
                ],

                "answer":
                    "Zero",

                "explanation":
                    "The upward and downward forces are equal and opposite, so they cancel. The net force is zero and the book does not accelerate."
            }
        },


        # -------------------------------------------------
        # NEWTON FIRST LAW
        # -------------------------------------------------

        {
            "order": 30,

            "type": "real_world",

            "heading":
                "Newton's First Law — The Law of Inertia",

            "body": """
Newton's First Law explains what happens
when the net external force is zero.


THE LAW

An object at rest remains at rest,
and an object in motion continues moving
with constant velocity,

unless acted upon by a net external force.


INERTIA

Inertia is the tendency of an object
to resist a change in its state of motion.


REAL-WORLD STORY

You are sitting inside a moving car.

Suddenly the driver presses the brakes.

The car slows quickly.

But your body tends to continue moving forward.

Why?

Because your body has inertia.


SEAT BELT CONNECTION

The seat belt provides the force required
to stop your body safely with the car.


ANOTHER EXAMPLE

A football lying on the ground
does not start moving by itself.

It remains at rest until a force acts on it.


IMPORTANT

More mass generally means more inertia.

A heavy object is harder to accelerate
or stop than a lighter object.


ONE-LINE TAKEAWAY

Objects resist changes in their motion.

That resistance is inertia.
""",

            "media_url":
                "/uploads/notes/physics/topic_3/newton_first_law_inertia.svg",

            "media_type":
                "svg",

            "caption":
                "When a car suddenly brakes, the passenger's body tends to continue moving forward because of inertia.",

            "alt_text":
                "Passenger moving forward when a car suddenly brakes."
        },


        # -------------------------------------------------
        # CHECK 2
        # -------------------------------------------------

        {
            "order": 35,

            "type": "checkpoint",

            "heading":
                "Quick Check 2 — Inertia",

            "body":
                "Connect Newton's First Law with everyday travel.",

            "interactive": {

                "question":
                    "Why does a passenger tend to move forward when a moving bus stops suddenly?",

                "options": [
                    "Because of inertia",
                    "Because gravity becomes stronger",
                    "Because friction disappears completely",
                    "Because the passenger becomes lighter"
                ],

                "answer":
                    "Because of inertia",

                "explanation":
                    "The passenger's body was moving with the bus and tends to continue in motion even when the bus suddenly stops. This resistance to change in motion is inertia."
            }
        },


        # -------------------------------------------------
        # NEWTON SECOND LAW
        # -------------------------------------------------

        {
            "order": 40,

            "type": "definition",

            "heading":
                "Newton's Second Law — Force, Mass and Acceleration",

            "body": """
Newton's Second Law tells us
how much an object accelerates
when a net force acts on it.


FORMULA

F = m × a


Where:

F = Net Force

m = Mass

a = Acceleration


SO:

a = F / m


WHAT DOES THIS MEAN?


CASE 1 — MORE FORCE

For the same mass:

More Force → More Acceleration


CASE 2 — MORE MASS

For the same force:

More Mass → Less Acceleration


EXAMPLE

Suppose:

Mass = 5 kg

Acceleration = 2 m/s²


Force:

F = m × a

F = 5 × 2

F = 10 N


REAL-WORLD EXAMPLE

Push an empty shopping cart.

It accelerates easily.

Now fill the same cart with heavy items.

Using the same push,
its acceleration becomes smaller.

Why?

The mass increased.


ONE-LINE TAKEAWAY

Force causes acceleration.

Greater force increases acceleration.

Greater mass reduces acceleration for the same force.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # CHECK 3
        # -------------------------------------------------

        {
            "order": 45,

            "type": "checkpoint",

            "heading":
                "Quick Check 3 — Use F = ma",

            "body":
                "Apply Newton's Second Law.",

            "interactive": {

                "question":
                    "A 4 kg object accelerates at 3 m/s². What net force acts on it?",

                "options": [
                    "7 N",
                    "12 N",
                    "1.33 N",
                    "24 N"
                ],

                "answer":
                    "12 N",

                "explanation":
                    "Using F = m × a, F = 4 × 3 = 12 N."
            }
        },


        # -------------------------------------------------
        # NEWTON THIRD LAW
        # -------------------------------------------------

        {
            "order": 50,

            "type": "animation",

            "heading":
                "Newton's Third Law — Action and Reaction",

            "body": """
Newton's Third Law describes forces
between interacting objects.


THE LAW

For every action,
there is an equal and opposite reaction.


IMPORTANT

Action and reaction forces:

• Are equal in magnitude
• Are opposite in direction
• Act on different objects


EXAMPLE — PUSHING A WALL

You push the wall.

ACTION:

Your hands push the wall.

REACTION:

The wall pushes your hands back.


EXAMPLE — WALKING

Your foot pushes the ground backward.

The ground pushes your foot forward.

That forward reaction force helps you move.


EXAMPLE — SWIMMING

A swimmer pushes water backward.

The water pushes the swimmer forward.


EXAMPLE — ROCKET

The rocket accelerates exhaust gases downward.

The gases exert an opposite force on the rocket.

The rocket moves upward.


IMPORTANT MISUNDERSTANDING

The action and reaction forces do not cancel each other
because they act on different objects.


ONE-LINE TAKEAWAY

Forces always occur as interaction pairs:
equal in size and opposite in direction.
""",

            "media_url":
                "/uploads/notes/physics/topic_3/newton_third_law.svg",

            "media_type":
                "svg",

            "caption":
                "When a person pushes the wall, the wall simultaneously pushes the person in the opposite direction.",

            "alt_text":
                "Action-reaction forces between a person and a wall."
        },


        # -------------------------------------------------
        # CHECK 4
        # -------------------------------------------------

        {
            "order": 55,

            "type": "checkpoint",

            "heading":
                "Quick Check 4 — Action and Reaction",

            "body":
                "Identify Newton's Third Law pair.",

            "interactive": {

                "question":
                    "When a swimmer pushes water backward, why does the swimmer move forward?",

                "options": [
                    "Water exerts an opposite forward force on the swimmer",
                    "Gravity pushes the swimmer forward",
                    "The swimmer loses all inertia",
                    "Water has no resistance"
                ],

                "answer":
                    "Water exerts an opposite forward force on the swimmer",

                "explanation":
                    "The swimmer pushes water backward, and the water exerts an equal and opposite force on the swimmer. This is Newton's Third Law."
            }
        },


        # -------------------------------------------------
        # APPLICATIONS
        # -------------------------------------------------

        {
            "order": 60,

            "type": "application",

            "heading":
                "Where Are Newton's Laws Used?",

            "body": """
🚗 VEHICLES

Engine force accelerates the vehicle.

Brakes provide force that reduces velocity.

Seat belts protect passengers because of inertia.


🏃 SPORTS

A football accelerates when kicked.

A heavier ball requires greater force
for the same acceleration.


🚀 ROCKETS

Exhaust gases are accelerated backward/downward.

The reaction force creates thrust.


🤖 ROBOTS

Robot motors generate forces and torques.

Controllers determine how much force is needed
to create the required acceleration.


🏗️ ENGINEERING

Engineers analyze forces when designing:

• Buildings
• Bridges
• Machines
• Vehicles
• Elevators
• Industrial robots


✈️ AIRCRAFT

Forces such as:

• Lift
• Weight
• Thrust
• Drag

control aircraft motion.


Newton's Laws provide the foundation
for understanding mechanical motion.
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
FORCE

A push or pull.

SI unit = Newton (N)


BALANCED FORCES

Net Force = 0

No acceleration.


UNBALANCED FORCES

Net Force ≠ 0

Acceleration occurs.


NEWTON'S FIRST LAW

An object resists changes in motion.

Key concept:

INERTIA


NEWTON'S SECOND LAW

F = m × a

Force produces acceleration.


NEWTON'S THIRD LAW

For every action,
there is an equal and opposite reaction.


FINAL CONNECTION

No net force
→ Motion stays unchanged.

Net force
→ Velocity changes.

More force
→ More acceleration.

More mass
→ More resistance to acceleration.

Interactions
→ Equal and opposite force pairs.


These three laws explain a huge part
of everyday mechanical motion.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        }

    ]


    # =====================================================
    # INSERT SECTIONS
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


    checkpoints = sum(
        1
        for section in saved_sections
        if section.section_type == "checkpoint"
    )


    print("")
    print("==========================================")
    print(" TOPIC 3 RICH NOTES CREATED SUCCESSFULLY")
    print("==========================================")
    print("")

    print(
        f"Topic ID : {topic.id}"
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
        f"Total checkpoints: {checkpoints}"
    )

    print("")

    print("Generated visuals:")

    print(
        MEDIA_DIR
        / "force_changes_motion.svg"
    )

    print(
        MEDIA_DIR
        / "newton_first_law_inertia.svg"
    )

    print(
        MEDIA_DIR
        / "newton_third_law.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 3 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()