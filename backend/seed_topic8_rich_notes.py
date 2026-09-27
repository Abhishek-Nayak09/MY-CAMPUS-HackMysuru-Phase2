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
    / "topic_8"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — MAGNETIC FIELD
# =========================================================

magnetic_field_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 470">

    <rect
        width="1000"
        height="470"
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
        Magnetic Field Around a Bar Magnet
    </text>

    <!-- MAGNET -->

    <rect
        x="365"
        y="195"
        width="135"
        height="80"
        rx="12"
        fill="#ef4444"
    />

    <rect
        x="500"
        y="195"
        width="135"
        height="80"
        rx="12"
        fill="#2563eb"
    />

    <text
        x="430"
        y="245"
        font-family="Arial"
        font-size="32"
        font-weight="700"
        text-anchor="middle"
        fill="white"
    >
        N
    </text>

    <text
        x="565"
        y="245"
        font-family="Arial"
        font-size="32"
        font-weight="700"
        text-anchor="middle"
        fill="white"
    >
        S
    </text>

    <!-- FIELD LINES -->

    <path
        d="M390 190 C300 85, 700 85, 610 190"
        fill="none"
        stroke="#7c3aed"
        stroke-width="5"
    />

    <path
        d="M380 180 C220 20, 780 20, 620 180"
        fill="none"
        stroke="#7c3aed"
        stroke-width="4"
    />

    <path
        d="M390 280 C300 385, 700 385, 610 280"
        fill="none"
        stroke="#7c3aed"
        stroke-width="5"
    />

    <path
        d="M380 290 C220 450, 780 450, 620 290"
        fill="none"
        stroke="#7c3aed"
        stroke-width="4"
    />

    <!-- MOVING FIELD DOTS -->

    <circle r="9" fill="#16a34a">
        <animateMotion
            dur="3s"
            repeatCount="indefinite"
            path="M390 190 C300 85, 700 85, 610 190"
        />
    </circle>

    <circle r="9" fill="#16a34a">
        <animateMotion
            dur="3s"
            repeatCount="indefinite"
            path="M390 280 C300 385, 700 385, 610 280"
        />
    </circle>

    <text
        x="250"
        y="420"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#4338ca"
    >
        Outside the magnet: field direction is N → S
    </text>

</svg>
"""


# =========================================================
# SVG 2 — ELECTROMAGNET
# =========================================================

electromagnet_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 470">

    <rect
        width="1000"
        height="470"
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
        Electric Current Can Create Magnetism
    </text>

    <!-- IRON CORE -->

    <rect
        x="250"
        y="185"
        width="500"
        height="90"
        rx="20"
        fill="#64748b"
    />

    <text
        x="500"
        y="240"
        text-anchor="middle"
        font-family="Arial"
        font-size="22"
        fill="white"
    >
        Iron Core
    </text>

    <!-- COIL -->

    <g
        fill="none"
        stroke="#f59e0b"
        stroke-width="12"
    >

        <ellipse cx="300" cy="230" rx="24" ry="80"/>
        <ellipse cx="355" cy="230" rx="24" ry="80"/>
        <ellipse cx="410" cy="230" rx="24" ry="80"/>
        <ellipse cx="465" cy="230" rx="24" ry="80"/>
        <ellipse cx="520" cy="230" rx="24" ry="80"/>
        <ellipse cx="575" cy="230" rx="24" ry="80"/>
        <ellipse cx="630" cy="230" rx="24" ry="80"/>
        <ellipse cx="685" cy="230" rx="24" ry="80"/>

    </g>

    <!-- CURRENT INDICATOR -->

    <circle
        r="10"
        fill="#ef4444"
    >
        <animateMotion
            dur="2.5s"
            repeatCount="indefinite"
            path="M235 145 L760 145"
        />
    </circle>

    <line
        x1="235"
        y1="145"
        x2="760"
        y2="145"
        stroke="#ef4444"
        stroke-width="5"
    />

    <text
        x="400"
        y="120"
        font-family="Arial"
        font-size="20"
        fill="#b91c1c"
    >
        Electric Current
    </text>

    <!-- POLES -->

    <text
        x="205"
        y="240"
        font-family="Arial"
        font-size="30"
        font-weight="700"
        fill="#dc2626"
    >
        N
    </text>

    <text
        x="790"
        y="240"
        font-family="Arial"
        font-size="30"
        font-weight="700"
        fill="#2563eb"
    >
        S
    </text>

    <text
        x="205"
        y="390"
        font-family="Arial"
        font-size="23"
        font-weight="700"
        fill="#15803d"
    >
        Current through coil → Magnetic field → Electromagnet
    </text>

</svg>
"""


# =========================================================
# SVG 3 — MOTOR / GENERATOR CONNECTION
# =========================================================

motor_generator_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 470">

    <rect
        width="1000"
        height="470"
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
        Electricity and Magnetism Work Both Ways
    </text>

    <!-- MOTOR -->

    <rect
        x="90"
        y="125"
        width="350"
        height="245"
        rx="24"
        fill="#ffffff"
        stroke="#fdba74"
        stroke-width="4"
    />

    <text
        x="265"
        y="175"
        text-anchor="middle"
        font-family="Arial"
        font-size="27"
        font-weight="700"
        fill="#ea580c"
    >
        ELECTRIC MOTOR
    </text>

    <text
        x="265"
        y="235"
        text-anchor="middle"
        font-family="Arial"
        font-size="21"
        fill="#172033"
    >
        Electrical Energy
    </text>

    <text
        x="265"
        y="275"
        text-anchor="middle"
        font-family="Arial"
        font-size="34"
        font-weight="700"
        fill="#7c3aed"
    >
        ↓
    </text>

    <text
        x="265"
        y="325"
        text-anchor="middle"
        font-family="Arial"
        font-size="21"
        fill="#172033"
    >
        Mechanical Motion
    </text>

    <!-- GENERATOR -->

    <rect
        x="560"
        y="125"
        width="350"
        height="245"
        rx="24"
        fill="#ffffff"
        stroke="#86efac"
        stroke-width="4"
    />

    <text
        x="735"
        y="175"
        text-anchor="middle"
        font-family="Arial"
        font-size="27"
        font-weight="700"
        fill="#15803d"
    >
        GENERATOR
    </text>

    <text
        x="735"
        y="235"
        text-anchor="middle"
        font-family="Arial"
        font-size="21"
        fill="#172033"
    >
        Mechanical Motion
    </text>

    <text
        x="735"
        y="275"
        text-anchor="middle"
        font-family="Arial"
        font-size="34"
        font-weight="700"
        fill="#7c3aed"
    >
        ↓
    </text>

    <text
        x="735"
        y="325"
        text-anchor="middle"
        font-family="Arial"
        font-size="21"
        fill="#172033"
    >
        Electrical Energy
    </text>

    <text
        x="245"
        y="425"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#172033"
    >
        Electromagnetism connects electricity with mechanical motion
    </text>

</svg>
"""


# =========================================================
# SAVE VISUALS
# =========================================================

(
    MEDIA_DIR
    / "magnetic_field.svg"
).write_text(
    magnetic_field_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "electromagnet.svg"
).write_text(
    electromagnet_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "motor_generator.svg"
).write_text(
    motor_generator_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # TOPIC 8
    # =====================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == 8
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 8 not found."
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

            topic_id=topic.id,

            created_by=None,

            title=
                "Magnetism & Electromagnetism",

            subtitle=
                "Understand magnetic fields, electromagnets and how electricity can create motion.",

            introduction=
                "Magnets attract objects without touching them. Electric current can also create magnetic fields, and this connection between electricity and magnetism is what makes motors, generators, speakers and many modern machines possible.",

            pdf_url=None,

            version=1,

            is_active=True
        )


        db.add(note)

        db.commit()

        db.refresh(note)


    else:

        note.title = (
            "Magnetism & Electromagnetism"
        )

        note.subtitle = (
            "Understand magnetic fields, electromagnets and how electricity can create motion."
        )

        note.introduction = (
            "Magnets attract objects without touching them. Electric current can also create magnetic fields, and this connection between electricity and magnetism is what makes motors, generators, speakers and many modern machines possible."
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
        # MAGNET STORY
        # -------------------------------------------------

        {
            "order": 10,

            "type": "story",

            "heading":
                "How Can a Magnet Pull Something Without Touching It?",

            "body": """
Place a magnet close to an iron object.

Before the magnet even touches it,
the iron object may begin moving.

How can this happen?

The magnet creates a MAGNETIC FIELD
in the space around it.


MAGNETIC FIELD

A magnetic field is a region
where magnetic forces can act.


Every bar magnet has two poles:

• North Pole
• South Pole


POLE INTERACTION

Unlike poles attract:

North + South
→ Attraction


Like poles repel:

North + North
→ Repulsion

South + South
→ Repulsion


MAGNETIC FIELD LINES

Outside a bar magnet,
field lines are conventionally shown travelling:

North
→ South


The field is generally strongest
near the poles.


ONE-LINE TAKEAWAY

A magnetic field allows magnetic forces
to act without direct contact.
""",

            "media_url":
                "/uploads/notes/physics/topic_8/magnetic_field.svg",

            "media_type":
                "svg",

            "caption":
                "Magnetic field lines outside a bar magnet are conventionally directed from north to south.",

            "alt_text":
                "Animated magnetic field lines surrounding a bar magnet."
        },


        # -------------------------------------------------
        # CHECK 1
        # -------------------------------------------------

        {
            "order": 15,

            "type": "checkpoint",

            "heading":
                "Quick Check 1 — Magnetic Poles",

            "body":
                "Remember how magnetic poles interact.",

            "interactive": {

                "question":
                    "What happens when the north pole of one magnet is brought near the south pole of another magnet?",

                "options": [
                    "They attract",
                    "They repel",
                    "Both magnets lose magnetism immediately",
                    "Nothing can happen without contact"
                ],

                "answer":
                    "They attract",

                "explanation":
                    "Unlike magnetic poles attract each other, while like poles repel."
            }
        },


        # -------------------------------------------------
        # EARTH / COMPASS
        # -------------------------------------------------

        {
            "order": 20,

            "type": "real_world",

            "heading":
                "The Earth Behaves Like a Giant Magnetic System",

            "body": """
A compass contains a small magnetic needle.

When free to rotate,
the needle aligns approximately
with Earth's magnetic field.


This is why a compass can help
indicate direction.


REAL-WORLD CONNECTION

Magnetic navigation has been used
for centuries.

Today magnetic-field sensors are also found
inside devices such as:

• Smartphones
• Navigation systems
• Robotics platforms
• Drones


These sensors are often called:

MAGNETOMETERS.


A magnetometer can measure
the strength and direction
of magnetic fields.


ROBOTICS CONNECTION

A mobile robot can combine information from:

• Magnetometer
• Gyroscope
• Accelerometer
• Encoders

to estimate its orientation and motion.


ONE-LINE TAKEAWAY

Earth's magnetic field provides
a natural directional reference.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # CURRENT CREATES FIELD
        # -------------------------------------------------

        {
            "order": 30,

            "type": "definition",

            "heading":
                "Electric Current Creates a Magnetic Field",

            "body": """
Electricity and magnetism are closely connected.


When electric current flows through a wire,
a magnetic field forms around that wire.


This was a major discovery
in understanding electromagnetism.


STRAIGHT WIRE

Current through a straight conductor
produces circular magnetic field lines
around the wire.


DIRECTION

The magnetic-field direction
depends on the direction of current.


RIGHT-HAND RULE

A useful rule is:

Point your right thumb
in the direction of conventional current.

Your curled fingers indicate
the direction of the magnetic field
around the wire.


IMPORTANT CONNECTION

No current:

No current-produced magnetic field.


Current flows:

Magnetic field appears around conductor.


ONE-LINE TAKEAWAY

Moving electric charge produces
a magnetic field.
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
                "Quick Check 2 — Current and Magnetism",

            "body":
                "Connect electricity with magnetic fields.",

            "interactive": {

                "question":
                    "What happens around a wire when electric current flows through it?",

                "options": [
                    "A magnetic field is produced",
                    "Gravity disappears",
                    "The wire becomes massless",
                    "Electric current automatically becomes zero"
                ],

                "answer":
                    "A magnetic field is produced",

                "explanation":
                    "An electric current produces a magnetic field around the conductor. This is one of the fundamental links between electricity and magnetism."
            }
        },


        # -------------------------------------------------
        # ELECTROMAGNET
        # -------------------------------------------------

        {
            "order": 40,

            "type": "animation",

            "heading":
                "Electromagnets — Magnets We Can Control",

            "body": """
Suppose we wind a wire into many loops
and allow current to flow through it.

The magnetic effects of the loops combine.

This forms a strong magnetic field.


A coil of wire is often called a:

SOLENOID.


If we place a suitable iron core
inside the coil,
the magnetic effect becomes much stronger.


This forms an:

ELECTROMAGNET.


WHY ELECTROMAGNETS ARE SPECIAL

Unlike many permanent magnets,
an electromagnet can be controlled.


Current ON:

Magnetic field produced.


Current OFF:

Magnetic effect greatly reduces.


HOW TO INCREASE ELECTROMAGNET STRENGTH

We can generally increase it by:

• Increasing current
• Increasing number of coil turns
• Using a suitable ferromagnetic core


REAL-WORLD USE

Electromagnets are found in:

• Relays
• Electric bells
• Solenoids
• Magnetic locks
• Industrial lifting magnets
• Motors
• Speakers


ONE-LINE TAKEAWAY

An electromagnet converts electric current
into a controllable magnetic field.
""",

            "media_url":
                "/uploads/notes/physics/topic_8/electromagnet.svg",

            "media_type":
                "svg",

            "caption":
                "Current through a coil creates a magnetic field; adding an iron core can strengthen the electromagnet.",

            "alt_text":
                "Animated solenoid carrying current around an iron core."
        },


        # -------------------------------------------------
        # CHECK 3
        # -------------------------------------------------

        {
            "order": 45,

            "type": "checkpoint",

            "heading":
                "Quick Check 3 — Stronger Electromagnet",

            "body":
                "Think about what strengthens the magnetic field.",

            "interactive": {

                "question":
                    "Which change can generally make an electromagnet stronger?",

                "options": [
                    "Increasing the current through the coil",
                    "Removing all current",
                    "Breaking the electrical circuit",
                    "Reducing the coil to zero turns"
                ],

                "answer":
                    "Increasing the current through the coil",

                "explanation":
                    "Increasing current generally increases the magnetic field produced by the coil. More turns and a suitable iron core can also strengthen an electromagnet."
            }
        },


        # -------------------------------------------------
        # MOTOR EFFECT
        # -------------------------------------------------

        {
            "order": 50,

            "type": "real_world",

            "heading":
                "Electric Motor — From Electricity to Motion",

            "body": """
Now we have two important ideas:

1. Electric current creates a magnetic field.

2. Magnetic fields can exert forces.


Put them together,
and we can create MOTION.


MOTOR PRINCIPLE

A current-carrying conductor placed
in a magnetic field can experience a force.


In an electric motor,
forces on current-carrying coils
produce rotational motion.


ENERGY CONVERSION

Electrical Energy
→ Mechanical Energy


REAL-WORLD EXAMPLES

Electric motors are found in:

• Fans
• Pumps
• Washing machines
• Electric vehicles
• Drones
• Industrial robots
• Computer cooling fans
• Robotic wheels


ROBOTICS CONNECTION

When a robot motor receives electrical current:

Electrical energy enters the motor.

Electromagnetic forces produce torque.

The shaft rotates.

That rotation drives:

• Wheels
• Gears
• Arms
• Pumps
• Other mechanisms


ONE-LINE TAKEAWAY

Electric motors use magnetic forces
to convert electricity into motion.
""",

            "media_url":
                "/uploads/notes/physics/topic_8/motor_generator.svg",

            "media_type":
                "svg",

            "caption":
                "Motors convert electrical energy to motion, while generators perform the reverse energy conversion.",

            "alt_text":
                "Diagram comparing energy conversion in electric motors and generators."
        },


        # -------------------------------------------------
        # ELECTROMAGNETIC INDUCTION
        # -------------------------------------------------

        {
            "order": 60,

            "type": "definition",

            "heading":
                "Electromagnetic Induction — Motion Can Produce Electricity",

            "body": """
The electricity-magnetism relationship
also works in another important way.


A CHANGING MAGNETIC ENVIRONMENT
can induce an electrical effect in a conductor.


This phenomenon is called:

ELECTROMAGNETIC INDUCTION.


A common example:

Move a magnet relative to a coil.

The magnetic field through the coil changes.

A voltage can be induced.


GENERATOR PRINCIPLE

Generators use electromagnetic induction
to convert:

Mechanical Energy
→ Electrical Energy


HOW?

Mechanical motion rotates or moves
conductors relative to magnetic fields.

This changing magnetic situation
induces electrical voltage.


REAL-WORLD APPLICATIONS

• Power stations
• Wind turbines
• Hydroelectric generators
• Bicycle dynamos
• Alternators
• Wireless charging principles


IMPORTANT CONNECTION

MOTOR:

Electricity
→ Motion


GENERATOR:

Motion
→ Electricity


ONE-LINE TAKEAWAY

Changing magnetic fields can produce
electrical voltage.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # CHECK 4
        # -------------------------------------------------

        {
            "order": 65,

            "type": "checkpoint",

            "heading":
                "Quick Check 4 — Motor or Generator?",

            "body":
                "Identify the direction of energy conversion.",

            "interactive": {

                "question":
                    "Which device mainly converts mechanical energy into electrical energy using electromagnetic induction?",

                "options": [
                    "Generator",
                    "Electric motor",
                    "Permanent resistor",
                    "Simple switch"
                ],

                "answer":
                    "Generator",

                "explanation":
                    "A generator converts mechanical energy into electrical energy using electromagnetic induction. A motor mainly performs the opposite conversion."
            }
        },


        # -------------------------------------------------
        # APPLICATIONS
        # -------------------------------------------------

        {
            "order": 70,

            "type": "application",

            "heading":
                "Where Is Electromagnetism Used?",

            "body": """
🤖 ROBOTICS

Electric motors move:

• Wheels
• Robot arms
• Grippers
• Conveyors


🔊 SPEAKERS

Electrical signals pass through coils.

Electromagnetic forces move the speaker cone.

The cone produces sound vibrations.


⚡ GENERATORS

Mechanical motion produces electrical energy.


🚗 ELECTRIC VEHICLES

Power electronics supply current
to electric motors.

Electromagnetic forces produce wheel torque.


🏭 INDUSTRIAL AUTOMATION

Solenoids and relays use electromagnetism
for switching and mechanical actuation.


🧲 MAGNETIC LIFTING

Large electromagnets can lift
ferromagnetic materials in factories
and scrapyards.


💳 DATA AND SENSING

Magnetic principles are used in
many sensing and data-storage technologies.


🏥 MEDICAL TECHNOLOGY

Strong controlled magnetic fields
are important in technologies such as MRI.


Electromagnetism is therefore one of
the foundations of modern electrical engineering.
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
MAGNET

Has:

North pole

and

South pole.


POLES

Unlike poles attract.

Like poles repel.


MAGNETIC FIELD

Region where magnetic forces can act.


FIELD DIRECTION

Outside a bar magnet:

N → S


CURRENT AND MAGNETISM

Electric current produces
a magnetic field.


ELECTROMAGNET

Current through a coil
creates controllable magnetism.

Strength can generally increase with:

• More current
• More coil turns
• Suitable magnetic core


ELECTRIC MOTOR

Electrical Energy
→ Mechanical Energy


ELECTROMAGNETIC INDUCTION

Changing magnetic environment
can induce voltage.


GENERATOR

Mechanical Energy
→ Electrical Energy


FINAL CONNECTION

Magnet
→ Magnetic field

Current
→ Magnetic field

Current + Coil
→ Electromagnet

Current + Magnetic field
→ Mechanical force

Motor
→ Electricity becomes motion

Changing magnetic field
→ Induced voltage

Generator
→ Motion becomes electricity


Electromagnetism connects
electricity, magnetism and mechanical motion.
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


    checkpoint_count = sum(
        1
        for section in saved_sections
        if section.section_type == "checkpoint"
    )


    print("")
    print("==========================================")
    print(" TOPIC 8 RICH NOTES CREATED SUCCESSFULLY")
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
        / "magnetic_field.svg"
    )

    print(
        MEDIA_DIR
        / "electromagnet.svg"
    )

    print(
        MEDIA_DIR
        / "motor_generator.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 8 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()