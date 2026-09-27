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
# MEDIA DIRECTORY
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parent

MEDIA_DIR = (
    BACKEND_DIR
    / "uploads"
    / "notes"
    / "physics"
    / "topic_2"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — DISTANCE VS DISPLACEMENT
# =========================================================

distance_svg = """
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
        Distance vs Displacement
    </text>

    <!-- START -->

    <circle
        cx="130"
        cy="310"
        r="18"
        fill="#22c55e"
    />

    <text
        x="100"
        y="350"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Start
    </text>

    <!-- END -->

    <circle
        cx="820"
        cy="160"
        r="18"
        fill="#ef4444"
    />

    <text
        x="800"
        y="130"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        End
    </text>

    <!-- CURVED DISTANCE -->

    <path
        d="M130 310
           C260 100,
            400 390,
            560 180
           C660 70,
            730 260,
            820 160"
        fill="none"
        stroke="#6366f1"
        stroke-width="8"
        stroke-dasharray="15 10"
    />

    <!-- DISPLACEMENT -->

    <line
        x1="130"
        y1="310"
        x2="820"
        y2="160"
        stroke="#f97316"
        stroke-width="7"
    />

    <polygon
        points="820,160 790,150 800,180"
        fill="#f97316"
    />

    <text
        x="380"
        y="120"
        font-family="Arial"
        font-size="21"
        fill="#4f46e5"
    >
        Actual path travelled = Distance
    </text>

    <text
        x="430"
        y="300"
        font-family="Arial"
        font-size="21"
        fill="#ea580c"
    >
        Shortest straight path = Displacement
    </text>

</svg>
"""


# =========================================================
# SVG 2 — SPEED VS VELOCITY
# =========================================================

speed_svg = """
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
        Speed vs Velocity
    </text>

    <!-- ROAD -->

    <line
        x1="80"
        y1="290"
        x2="910"
        y2="290"
        stroke="#64748b"
        stroke-width="8"
    />

    <line
        x1="80"
        y1="315"
        x2="910"
        y2="315"
        stroke="#cbd5e1"
        stroke-width="5"
        stroke-dasharray="25 20"
    />

    <!-- CAR -->

    <g>

        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0;500 0;0 0"
            dur="5s"
            repeatCount="indefinite"
        />

        <rect
            x="120"
            y="220"
            width="190"
            height="65"
            rx="22"
            fill="#4f46e5"
        />

        <circle
            cx="160"
            cy="290"
            r="24"
            fill="#111827"
        />

        <circle
            cx="270"
            cy="290"
            r="24"
            fill="#111827"
        />

    </g>

    <!-- DIRECTION ARROW -->

    <line
        x1="380"
        y1="150"
        x2="650"
        y2="150"
        stroke="#dc2626"
        stroke-width="8"
    />

    <polygon
        points="670,150 635,130 635,170"
        fill="#dc2626"
    />

    <text
        x="390"
        y="125"
        font-family="Arial"
        font-size="21"
        fill="#dc2626"
    >
        Direction matters for Velocity
    </text>

    <text
        x="100"
        y="390"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Speed = how fast
    </text>

    <text
        x="580"
        y="390"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Velocity = how fast + direction
    </text>

</svg>
"""


# =========================================================
# SVG 3 — MOTION STORY
# =========================================================

motion_svg = """
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
        Your Journey to College
    </text>

    <!-- HOUSE -->

    <rect
        x="90"
        y="220"
        width="130"
        height="110"
        fill="#60a5fa"
    />

    <polygon
        points="70,220 155,150 240,220"
        fill="#2563eb"
    />

    <text
        x="115"
        y="365"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Home
    </text>

    <!-- COLLEGE -->

    <rect
        x="770"
        y="175"
        width="150"
        height="155"
        fill="#a78bfa"
    />

    <rect
        x="825"
        y="260"
        width="40"
        height="70"
        fill="#4c1d95"
    />

    <text
        x="795"
        y="365"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        College
    </text>

    <!-- ROAD -->

    <path
        d="M220 290 Q500 110 770 280"
        fill="none"
        stroke="#64748b"
        stroke-width="16"
    />

    <!-- MOVING CAR -->

    <g>

        <animateMotion
            dur="5s"
            repeatCount="indefinite"
            path="M220 260 Q500 80 740 250"
        />

        <rect
            x="0"
            y="0"
            width="100"
            height="40"
            rx="14"
            fill="#ef4444"
        />

        <circle
            cx="22"
            cy="42"
            r="13"
            fill="#111827"
        />

        <circle
            cx="78"
            cy="42"
            r="13"
            fill="#111827"
        />

    </g>

    <text
        x="335"
        y="390"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Position changes with time → Motion
    </text>

</svg>
"""


# =========================================================
# SAVE SVG FILES
# =========================================================

(MEDIA_DIR / "distance_displacement.svg").write_text(
    distance_svg,
    encoding="utf-8"
)

(MEDIA_DIR / "speed_velocity.svg").write_text(
    speed_svg,
    encoding="utf-8"
)

(MEDIA_DIR / "motion_story.svg").write_text(
    motion_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # FIND TOPIC 2
    # =====================================================

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


    # =====================================================
    # FIND / CREATE NOTE
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
                "Motion, Distance, Speed & Velocity",

            subtitle=
                "Understand how we describe movement in the real world.",

            introduction=
                "From walking to college to tracking a car on Google Maps, motion is everywhere. Let us understand how Physics measures and describes it.",

            pdf_url=None,

            version=1,

            is_active=True
        )

        db.add(note)

        db.commit()

        db.refresh(note)

    else:

        note.title = (
            "Motion, Distance, Speed & Velocity"
        )

        note.subtitle = (
            "Understand how we describe movement in the real world."
        )

        note.introduction = (
            "From walking to college to tracking a car on Google Maps, motion is everywhere. Let us understand how Physics measures and describes it."
        )

        db.commit()


    # =====================================================
    # REMOVE OLD TOPIC 2 SECTIONS
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
    # SECTION DATA
    # =====================================================

    sections = [

        # =================================================
        # STORY
        # =================================================

        {
            "order": 10,
            "type": "story",
            "heading": "A Simple Journey to College",
            "body": """
Imagine you leave your house at 8:00 AM.

At 8:05 AM you are near the bus stop.

At 8:20 AM you are halfway to college.

At 8:35 AM you reach college.

Your position has changed with time.

That means you were in MOTION.


WHAT IS MOTION?

An object is said to be in motion when its position changes
with time relative to a reference point.


Example:

A bus moving past a tree is in motion relative to the tree.

But a passenger sitting inside that bus may appear stationary
relative to another passenger sitting next to them.


PHYSICS CONNECTION

Motion depends on:

• Position
• Time
• Reference point


ONE-LINE TAKEAWAY

Motion means change in position with time.
""",

            "media_url":
                "/uploads/notes/physics/topic_2/motion_story.svg",

            "media_type":
                "svg",

            "caption":
                "When your position changes from home to college as time passes, you are in motion.",

            "alt_text":
                "Animated journey from home to college showing motion."
        },


        # =================================================
        # DISTANCE / DISPLACEMENT
        # =================================================

        {
            "order": 20,
            "type": "concept",
            "heading": "Distance and Displacement — Are They the Same?",
            "body": """
No.

They describe movement differently.


DISTANCE

Distance is the total length of the actual path travelled.

It does not care about direction.

Distance is a SCALAR quantity.


Example:

Suppose you walk:

300 m east
then
200 m north.

Total distance travelled:

300 + 200 = 500 m


DISPLACEMENT

Displacement is the shortest straight-line change
from starting position to final position.

Direction is important.

Displacement is a VECTOR quantity.


IMPORTANT DIFFERENCE

Distance asks:

“How much path did you travel?”

Displacement asks:

“How far and in which direction are you from where you started?”


SPECIAL CASE

If you leave home,
walk around,
and finally return home:

Distance > 0

but

Displacement = 0


ONE-LINE TAKEAWAY

Distance measures the whole path.

Displacement measures the straight-line change in position.
""",

            "media_url":
                "/uploads/notes/physics/topic_2/distance_displacement.svg",

            "media_type":
                "svg",

            "caption":
                "The blue curved path shows distance; the orange straight line shows displacement.",

            "alt_text":
                "Diagram comparing distance and displacement."
        },


        # =================================================
        # CHECKPOINT 1
        # =================================================

        {
            "order": 25,
            "type": "checkpoint",
            "heading": "Quick Check 1 — Distance or Displacement?",
            "body":
                "Test the difference between total path and change in position.",

            "interactive":
                {
                    "question":
                        "A student walks 100 m from home to a shop and then walks 100 m back home. What is the displacement?",

                    "options": [
                        "200 m",
                        "100 m",
                        "0 m",
                        "50 m"
                    ],

                    "answer":
                        "0 m",

                    "explanation":
                        "The student finishes at the same position where the journey started. Therefore the change in position is zero, so displacement is 0 m. The total distance is 200 m."
                }
        },


        # =================================================
        # SPEED
        # =================================================

        {
            "order": 30,
            "type": "definition",
            "heading": "Speed — How Fast Are You Moving?",
            "body": """
Speed tells us how quickly distance is covered.


FORMULA

Speed = Distance / Time


SI UNIT

metre per second

m/s


EXAMPLE

A car travels 100 metres in 5 seconds.

Speed = 100 / 5

Speed = 20 m/s


WHAT SPEED TELLS US

A higher speed means more distance is covered
in the same amount of time.


REAL-WORLD EXAMPLES

• Car speedometer
• Running speed
• Train speed
• Internet data speed uses a different measurement idea,
  but also represents a rate
• Conveyor belt speed


IMPORTANT

Speed has magnitude only.

It does not tell us direction.

Therefore speed is a SCALAR quantity.


ONE-LINE TAKEAWAY

Speed tells us how fast an object covers distance.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # =================================================
        # VELOCITY
        # =================================================

        {
            "order": 40,
            "type": "real_world",
            "heading": "Velocity — Speed With Direction",
            "body": """
Velocity describes how quickly displacement changes with time.


FORMULA

Velocity = Displacement / Time


The important word is:

DIRECTION.


Example:

20 m/s

This describes SPEED.


20 m/s EAST

This describes VELOCITY.


WHY DIRECTION MATTERS

Imagine two cars.

Car A travels:

60 km/h east.

Car B travels:

60 km/h west.

Both have the same speed.

But they have different velocities
because their directions are different.


PHYSICS CONNECTION

Speed = magnitude only.

Velocity = magnitude + direction.


ONE-LINE TAKEAWAY

Velocity tells us both how fast an object moves
and the direction in which it moves.
""",

            "media_url":
                "/uploads/notes/physics/topic_2/speed_velocity.svg",

            "media_type":
                "svg",

            "caption":
                "Speed tells how fast; velocity includes both speed and direction.",

            "alt_text":
                "Animated car demonstrating speed and velocity."
        },


        # =================================================
        # CHECKPOINT 2
        # =================================================

        {
            "order": 45,
            "type": "checkpoint",
            "heading": "Quick Check 2 — Speed or Velocity?",
            "body":
                "Check whether direction changes the quantity.",

            "interactive":
                {
                    "question":
                        "Which of the following correctly describes velocity?",

                    "options": [
                        "50 km/h",
                        "10 metres",
                        "50 km/h north",
                        "5 seconds"
                    ],

                    "answer":
                        "50 km/h north",

                    "explanation":
                        "Velocity requires both magnitude and direction. '50 km/h north' tells us how fast the object moves and its direction."
                }
        },


        # =================================================
        # AVERAGE SPEED
        # =================================================

        {
            "order": 50,
            "type": "application",
            "heading": "Average Speed — Your Whole Journey",
            "body": """
Real journeys rarely happen at one constant speed.

You may:

• Stop at traffic signals
• Slow down near turns
• Accelerate on open roads
• Wait in traffic

So Physics often uses AVERAGE SPEED.


FORMULA

Average Speed
=
Total Distance Travelled
/
Total Time Taken


EXAMPLE

Suppose you travel:

120 km in 2 hours.

Average Speed:

120 / 2

= 60 km/h


IMPORTANT

Do not simply average two speeds
unless the conditions make that mathematically valid.

For most journey problems:

Always use

TOTAL DISTANCE / TOTAL TIME.


REAL-WORLD CONNECTION

Google Maps uses travel distance and estimated travel time
to help estimate journey speed and arrival time.


ONE-LINE TAKEAWAY

Average speed describes the overall rate of motion
for the complete journey.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # =================================================
        # CHECKPOINT 3
        # =================================================

        {
            "order": 55,
            "type": "checkpoint",
            "heading": "Quick Check 3 — Calculate Average Speed",
            "body":
                "Use Total Distance divided by Total Time.",

            "interactive":
                {
                    "question":
                        "A bike travels 150 km in 3 hours. What is its average speed?",

                    "options": [
                        "30 km/h",
                        "50 km/h",
                        "75 km/h",
                        "450 km/h"
                    ],

                    "answer":
                        "50 km/h",

                    "explanation":
                        "Average Speed = Total Distance / Total Time = 150 / 3 = 50 km/h."
                }
        },


        # =================================================
        # REAL WORLD TECHNOLOGY
        # =================================================

        {
            "order": 60,
            "type": "application",
            "heading": "Where Do We Use Motion, Speed and Velocity?",
            "body": """
🚗 VEHICLES

A speedometer shows the speed of a vehicle.


📱 GPS NAVIGATION

GPS tracks how your position changes with time.

This helps estimate:

• Speed
• Direction
• Travel route
• Arrival time


🏃 SPORTS

Athletes measure running speed.

Coaches analyze motion to improve performance.


✈️ AIRCRAFT

Pilots need both speed and direction.

Direction is critical,
so velocity becomes extremely important.


🚀 SPACECRAFT

Spacecraft navigation depends on extremely accurate
measurements of position and velocity.


🤖 ROBOTS

Robots use sensors and encoders
to estimate:

• Position
• Distance travelled
• Speed
• Direction of movement


Physics concepts of motion are therefore essential
for navigation and control systems.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # =================================================
        # CHECKPOINT 4
        # =================================================

        {
            "order": 70,
            "type": "checkpoint",
            "heading": "Quick Check 4 — Same Speed, Different Velocity",
            "body":
                "Direction can change velocity even when speed stays the same.",

            "interactive":
                {
                    "question":
                        "Two cars both travel at 60 km/h. One moves east and the other west. Which statement is correct?",

                    "options": [
                        "They have the same speed and same velocity",
                        "They have different speeds but same velocity",
                        "They have the same speed but different velocities",
                        "Both have zero velocity"
                    ],

                    "answer":
                        "They have the same speed but different velocities",

                    "explanation":
                        "Their speed magnitudes are equal at 60 km/h, but their directions are opposite. Since velocity includes direction, their velocities are different."
                }
        },


        # =================================================
        # SUMMARY
        # =================================================

        {
            "order": 80,
            "type": "summary",
            "heading": "What Should You Remember?",
            "body": """
MOTION

Change in position with time.


DISTANCE

Total path travelled.

Scalar quantity.


DISPLACEMENT

Shortest straight-line change from start to finish.

Vector quantity.


SPEED

Speed = Distance / Time

Tells how fast an object moves.


VELOCITY

Velocity = Displacement / Time

Tells how fast AND in which direction an object moves.


AVERAGE SPEED

Average Speed
=
Total Distance / Total Time


FINAL CONNECTION

Position changes with time
→ Motion

Measure the whole path
→ Distance

Measure change in position
→ Displacement

Distance divided by time
→ Speed

Displacement divided by time
→ Velocity


Once these ideas are clear,
the next topics such as acceleration,
force and Newton's Laws become much easier.
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


    print("")
    print("==========================================")
    print(" TOPIC 2 RICH NOTES CREATED SUCCESSFULLY")
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


    checkpoint_count = 0


    for section in saved_sections:

        print(
            f"{section.section_order}. "
            f"{section.section_type.upper()} "
            f"- {section.heading}"
        )

        if (
            section.section_type ==
            "checkpoint"
        ):

            checkpoint_count += 1


    print("")

    print(
        f"Total checkpoints: {checkpoint_count}"
    )

    print("")

    print("Generated visual assets:")

    print(
        MEDIA_DIR /
        "motion_story.svg"
    )

    print(
        MEDIA_DIR /
        "distance_displacement.svg"
    )

    print(
        MEDIA_DIR /
        "speed_velocity.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 2 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()