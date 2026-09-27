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
    / "topic_4"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — WORK
# =========================================================

work_svg = """
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
        Work = Force + Displacement
    </text>

    <!-- FLOOR -->

    <line
        x1="80"
        y1="330"
        x2="920"
        y2="330"
        stroke="#64748b"
        stroke-width="8"
    />

    <!-- BOX -->

    <g>

        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0;380 0;0 0"
            dur="5s"
            repeatCount="indefinite"
        />

        <rect
            x="180"
            y="235"
            width="130"
            height="90"
            rx="12"
            fill="#6366f1"
        />

        <text
            x="245"
            y="290"
            font-family="Arial"
            font-size="21"
            text-anchor="middle"
            fill="white"
        >
            BOX
        </text>

    </g>

    <!-- FORCE ARROW -->

    <line
        x1="90"
        y1="275"
        x2="165"
        y2="275"
        stroke="#dc2626"
        stroke-width="9"
    />

    <polygon
        points="180,275 150,255 150,295"
        fill="#dc2626"
    />

    <text
        x="85"
        y="240"
        font-family="Arial"
        font-size="21"
        fill="#dc2626"
    >
        Force
    </text>

    <!-- DISPLACEMENT -->

    <line
        x1="330"
        y1="185"
        x2="700"
        y2="185"
        stroke="#16a34a"
        stroke-width="8"
    />

    <polygon
        points="720,185 685,165 685,205"
        fill="#16a34a"
    />

    <text
        x="425"
        y="155"
        font-family="Arial"
        font-size="21"
        fill="#15803d"
    >
        Displacement
    </text>

    <text
        x="325"
        y="390"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#172033"
    >
        W = F × s   when force and motion are in the same direction
    </text>

</svg>
"""


# =========================================================
# SVG 2 — POTENTIAL TO KINETIC ENERGY
# =========================================================

energy_svg = """
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
        Energy Transformation
    </text>

    <!-- SLOPE -->

    <path
        d="M120 120 L820 330"
        stroke="#64748b"
        stroke-width="14"
        fill="none"
    />

    <!-- BALL -->

    <circle
        r="30"
        fill="#ef4444"
    >

        <animateMotion
            dur="4s"
            repeatCount="indefinite"
            path="M150 95 L790 290"
        />

    </circle>

    <!-- TOP -->

    <text
        x="120"
        y="185"
        font-family="Arial"
        font-size="21"
        font-weight="700"
        fill="#15803d"
    >
        High Position
    </text>

    <text
        x="120"
        y="215"
        font-family="Arial"
        font-size="19"
        fill="#15803d"
    >
        More Potential Energy
    </text>

    <!-- BOTTOM -->

    <text
        x="650"
        y="375"
        font-family="Arial"
        font-size="21"
        font-weight="700"
        fill="#b91c1c"
    >
        Faster Motion
    </text>

    <text
        x="650"
        y="405"
        font-family="Arial"
        font-size="19"
        fill="#b91c1c"
    >
        More Kinetic Energy
    </text>

    <text
        x="385"
        y="130"
        font-family="Arial"
        font-size="22"
        fill="#172033"
    >
        Potential Energy → Kinetic Energy
    </text>

</svg>
"""


# =========================================================
# SVG 3 — POWER
# =========================================================

power_svg = """
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
        Same Work — Different Power
    </text>

    <!-- STAIRS A -->

    <g>

        <rect x="100" y="310" width="70" height="40" fill="#94a3b8"/>
        <rect x="170" y="270" width="70" height="80" fill="#94a3b8"/>
        <rect x="240" y="230" width="70" height="120" fill="#94a3b8"/>
        <rect x="310" y="190" width="70" height="160" fill="#94a3b8"/>

        <circle cx="155" cy="245" r="25" fill="#2563eb"/>

        <text
            x="110"
            y="390"
            font-family="Arial"
            font-size="20"
            fill="#172033"
        >
            Person A: 10 s
        </text>

    </g>

    <!-- STAIRS B -->

    <g>

        <rect x="570" y="310" width="70" height="40" fill="#94a3b8"/>
        <rect x="640" y="270" width="70" height="80" fill="#94a3b8"/>
        <rect x="710" y="230" width="70" height="120" fill="#94a3b8"/>
        <rect x="780" y="190" width="70" height="160" fill="#94a3b8"/>

        <circle cx="825" cy="165" r="25" fill="#ef4444"/>

        <text
            x="585"
            y="390"
            font-family="Arial"
            font-size="20"
            fill="#172033"
        >
            Person B: 5 s
        </text>

    </g>

    <text
        x="310"
        y="115"
        font-family="Arial"
        font-size="23"
        font-weight="700"
        fill="#ea580c"
    >
        Less Time → Greater Power
    </text>

</svg>
"""


# =========================================================
# SAVE VISUALS
# =========================================================

(
    MEDIA_DIR
    / "work_force_displacement.svg"
).write_text(
    work_svg,
    encoding="utf-8"
)


(
    MEDIA_DIR
    / "energy_transformation.svg"
).write_text(
    energy_svg,
    encoding="utf-8"
)


(
    MEDIA_DIR
    / "power_comparison.svg"
).write_text(
    power_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # TOPIC 4 — USE ID DIRECTLY
    # =====================================================

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
                "Work, Energy & Power",

            subtitle=
                "Understand how forces transfer energy and how quickly work is done.",

            introduction=
                "Pushing a box, lifting a bag, climbing stairs and driving a vehicle all involve work, energy and power. These three ideas are closely connected.",

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
            "Work, Energy & Power"
        )

        note.subtitle = (
            "Understand how forces transfer energy and how quickly work is done."
        )

        note.introduction = (
            "Pushing a box, lifting a bag, climbing stairs and driving a vehicle all involve work, energy and power. These three ideas are closely connected."
        )

        db.commit()


    # =====================================================
    # DELETE OLD TOPIC 4 SECTIONS
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
        # WORK
        # -------------------------------------------------

        {
            "order": 10,

            "type": "story",

            "heading":
                "What Does 'Work' Mean in Physics?",

            "body": """
In everyday language we say:

“I worked all day.”

But Physics gives WORK a very specific meaning.


Imagine a box on the floor.

You push the box.

The box moves forward.

A force acted on the box,
and the box had displacement.

Therefore Physics says:

WORK WAS DONE.


BASIC FORMULA

When force and displacement are in the same direction:

W = F × s


Where:

W = Work

F = Force

s = Displacement


SI UNIT

Joule

Symbol:

J


EXAMPLE

You push a box with a force of 20 N.

The box moves 5 m in the direction of the force.

W = F × s

W = 20 × 5

W = 100 J


IMPORTANT CASE

Suppose you push a wall very hard.

But the wall does not move.

Displacement = 0

Therefore:

Work done on the wall = 0


ONE-LINE TAKEAWAY

In Physics, work requires both force AND displacement.
""",

            "media_url":
                "/uploads/notes/physics/topic_4/work_force_displacement.svg",

            "media_type":
                "svg",

            "caption":
                "A force does mechanical work when it produces displacement.",

            "alt_text":
                "Animated box moving due to an applied force, demonstrating mechanical work."
        },


        # -------------------------------------------------
        # CHECK 1
        # -------------------------------------------------

        {
            "order": 15,

            "type": "checkpoint",

            "heading":
                "Quick Check 1 — Was Work Done?",

            "body":
                "Remember: force alone is not enough.",

            "interactive": {

                "question":
                    "You push a rigid wall with a large force, but the wall does not move. How much mechanical work is done on the wall?",

                "options": [
                    "Zero",
                    "Very large",
                    "Equal to your force",
                    "Depends only on your body mass"
                ],

                "answer":
                    "Zero",

                "explanation":
                    "Mechanical work requires displacement. Since the wall does not move, displacement is zero and therefore W = F × 0 = 0."
            }
        },


        # -------------------------------------------------
        # ENERGY
        # -------------------------------------------------

        {
            "order": 20,

            "type": "definition",

            "heading":
                "Energy — The Ability to Do Work",

            "body": """
Energy is the ability to do work or cause change.


SI UNIT

Joule

Symbol:

J


Energy appears in many forms:

• Kinetic energy
• Potential energy
• Thermal energy
• Chemical energy
• Electrical energy
• Light energy
• Sound energy


IMPORTANT IDEA

Energy can move from one object to another.

It can also change from one form into another.


EXAMPLES

Battery:

Chemical Energy
→ Electrical Energy


Electric motor:

Electrical Energy
→ Mechanical Energy


Light bulb:

Electrical Energy
→ Light + Thermal Energy


Human body:

Chemical Energy from food
→ Movement + Heat


Energy connects many different areas of Physics.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # KINETIC ENERGY
        # -------------------------------------------------

        {
            "order": 30,

            "type": "real_world",

            "heading":
                "Kinetic Energy — Energy of Motion",

            "body": """
An object that is moving possesses kinetic energy.


FORMULA

KE = 1/2 × m × v²


Where:

m = Mass

v = Velocity


WHAT DOES THIS TELL US?


MORE MASS

A heavier moving object has more kinetic energy
than a lighter object moving at the same speed.


MORE SPEED

Speed has an even stronger effect
because velocity is squared.


EXAMPLE

Mass = 2 kg

Velocity = 3 m/s


KE = 1/2 × 2 × 3²

KE = 9 J


REAL-WORLD CONNECTION

A fast-moving car contains kinetic energy.

When the brakes are applied,
some of that kinetic energy is converted mainly
into thermal energy through friction.


IMPORTANT

Doubling speed does NOT merely double kinetic energy.

Because of v²,
kinetic energy increases much faster.


ONE-LINE TAKEAWAY

Moving objects possess kinetic energy.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # CHECK 2
        # -------------------------------------------------

        {
            "order": 35,

            "type": "checkpoint",

            "heading":
                "Quick Check 2 — Kinetic Energy",

            "body":
                "Use KE = 1/2 mv².",

            "interactive": {

                "question":
                    "A 2 kg object moves at 4 m/s. What is its kinetic energy?",

                "options": [
                    "4 J",
                    "8 J",
                    "16 J",
                    "32 J"
                ],

                "answer":
                    "16 J",

                "explanation":
                    "KE = 1/2 × m × v² = 1/2 × 2 × 4² = 16 J."
            }
        },


        # -------------------------------------------------
        # POTENTIAL ENERGY
        # -------------------------------------------------

        {
            "order": 40,

            "type": "animation",

            "heading":
                "Potential Energy — Stored Energy Due to Position",

            "body": """
An object can store energy because of its position.


GRAVITATIONAL POTENTIAL ENERGY

An object raised above the ground
can possess gravitational potential energy.


FORMULA

PE = m × g × h


Where:

m = Mass

g = Acceleration due to gravity

h = Height


EXAMPLE

Consider a ball held above the ground.

While the ball is held high:

It has gravitational potential energy.


When released:

The ball falls.

Potential Energy decreases.

Kinetic Energy increases.


ENERGY TRANSFORMATION

Potential Energy
→ Kinetic Energy


REAL-WORLD EXAMPLES

• Water stored behind a dam
• Roller coaster at the top of a hill
• Book kept on a shelf
• Lifted hammer
• Object raised by a crane


ONE-LINE TAKEAWAY

Height can store gravitational potential energy.
""",

            "media_url":
                "/uploads/notes/physics/topic_4/energy_transformation.svg",

            "media_type":
                "svg",

            "caption":
                "As the object moves downward, gravitational potential energy is converted into kinetic energy.",

            "alt_text":
                "Animated object moving down a slope while potential energy changes into kinetic energy."
        },


        # -------------------------------------------------
        # CONSERVATION
        # -------------------------------------------------

        {
            "order": 50,

            "type": "application",

            "heading":
                "Conservation of Energy — Energy Does Not Disappear",

            "body": """
One of the most important ideas in Physics is:

Energy cannot be created or destroyed.

It can only be transferred
or transformed from one form to another.


This is called:

THE LAW OF CONSERVATION OF ENERGY.


EXAMPLE — FALLING BALL

At the top:

Potential Energy is high.

Kinetic Energy is low.


While falling:

Potential Energy decreases.

Kinetic Energy increases.


Near the bottom:

Kinetic Energy is high.


REAL SYSTEMS

Some mechanical energy may become:

• Heat
• Sound
• Internal energy

because of friction and other effects.


CAR EXAMPLE

Fuel contains chemical energy.

Engine converts it into mechanical energy.

Vehicle gains kinetic energy.

Braking converts much of that kinetic energy
into thermal energy.


Energy changes form,
but it does not simply vanish.
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
            "order": 55,

            "type": "checkpoint",

            "heading":
                "Quick Check 3 — Energy Transformation",

            "body":
                "Follow the energy rather than assuming it disappears.",

            "interactive": {

                "question":
                    "A ball falls from a height. Ignoring air resistance, what mainly happens to its gravitational potential energy?",

                "options": [
                    "It disappears",
                    "It changes into kinetic energy",
                    "It changes only into mass",
                    "It becomes zero immediately"
                ],

                "answer":
                    "It changes into kinetic energy",

                "explanation":
                    "As the ball loses height, gravitational potential energy decreases while kinetic energy increases. Energy is transformed rather than destroyed."
            }
        },


        # -------------------------------------------------
        # POWER
        # -------------------------------------------------

        {
            "order": 60,

            "type": "real_world",

            "heading":
                "Power — How Quickly Is Work Done?",

            "body": """
Two people may perform the same amount of work.

But one person may finish much faster.

That difference is described by POWER.


FORMULA

Power = Work / Time


P = W / t


SI UNIT

Watt

Symbol:

W


EXAMPLE

A machine performs 1000 J of work in 5 seconds.


P = 1000 / 5

P = 200 W


STAIRCASE EXAMPLE

Person A climbs the stairs in 10 seconds.

Person B reaches the same height in 5 seconds.

If their masses are the same,
they perform approximately the same work against gravity.

But Person B performs that work in less time.

Therefore:

Person B produces greater power.


IMPORTANT

Power does not mean only
“how much work is done.”

It means:

“How quickly is the work done?”


ONE-LINE TAKEAWAY

More work per second means greater power.
""",

            "media_url":
                "/uploads/notes/physics/topic_4/power_comparison.svg",

            "media_type":
                "svg",

            "caption":
                "If the same work is completed in less time, the power is greater.",

            "alt_text":
                "Two people climbing the same stairs in different times to demonstrate power."
        },


        # -------------------------------------------------
        # CHECK 4
        # -------------------------------------------------

        {
            "order": 65,

            "type": "checkpoint",

            "heading":
                "Quick Check 4 — Calculate Power",

            "body":
                "Use P = W / t.",

            "interactive": {

                "question":
                    "A motor performs 600 J of work in 3 seconds. What is its power?",

                "options": [
                    "1800 W",
                    "603 W",
                    "200 W",
                    "20 W"
                ],

                "answer":
                    "200 W",

                "explanation":
                    "Power = Work / Time = 600 / 3 = 200 W."
            }
        },


        # -------------------------------------------------
        # APPLICATION
        # -------------------------------------------------

        {
            "order": 70,

            "type": "application",

            "heading":
                "Where Are Work, Energy and Power Used?",

            "body": """
🚗 VEHICLES

Fuel or batteries provide energy.

Motors and engines convert that energy
into vehicle motion.


⚡ ELECTRIC MOTORS

Electrical energy
→ Mechanical work


🏗️ CRANES

A crane performs work
while lifting heavy objects.

The lifted object gains potential energy.


🏃 HUMAN BODY

Food provides chemical energy.

Muscles transform it
into movement and heat.


💧 HYDROELECTRIC POWER

Water stored at height
possesses gravitational potential energy.

Moving water gains kinetic energy.

Turbines convert that energy into electricity.


🤖 ROBOTS

Motors consume electrical energy
and perform mechanical work.

Motor power determines how quickly
the actuator can perform work.


🏠 ELECTRICAL APPLIANCES

A 1000 W appliance uses/transfers energy
at a greater rate than a 100 W appliance.


These concepts are fundamental
to machines, vehicles, robotics and energy systems.
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
WORK

Requires force and displacement.

For same-direction force:

W = F × s

Unit = Joule


ENERGY

Ability to do work or cause change.

Unit = Joule


KINETIC ENERGY

Energy due to motion.

KE = 1/2 mv²


POTENTIAL ENERGY

Stored energy due to position.

For gravitational potential energy:

PE = mgh


CONSERVATION OF ENERGY

Energy cannot be created or destroyed.

It changes form or transfers between systems.


POWER

Rate at which work is done.

P = W / t

Unit = Watt


FINAL CONNECTION

Force + Displacement
→ Work

Ability to perform Work
→ Energy

Moving object
→ Kinetic Energy

Raised object
→ Potential Energy

Energy changes form
→ Conservation of Energy

Work completed faster
→ Greater Power
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
    print(" TOPIC 4 RICH NOTES CREATED SUCCESSFULLY")
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
        / "work_force_displacement.svg"
    )

    print(
        MEDIA_DIR
        / "energy_transformation.svg"
    )

    print(
        MEDIA_DIR
        / "power_comparison.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 4 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()