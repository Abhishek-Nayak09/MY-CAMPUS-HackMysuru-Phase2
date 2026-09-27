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
    / "topic_7"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — SIMPLE ELECTRIC CIRCUIT
# =========================================================

circuit_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 450">

    <rect
        width="1000"
        height="450"
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
        A Simple Electric Circuit
    </text>

    <!-- WIRES -->

    <path
        d="M180 220
           L180 120
           L760 120
           L760 220"
        fill="none"
        stroke="#334155"
        stroke-width="8"
    />

    <path
        d="M760 300
           L760 350
           L180 350
           L180 300"
        fill="none"
        stroke="#334155"
        stroke-width="8"
    />

    <!-- BATTERY -->

    <line
        x1="150"
        y1="220"
        x2="210"
        y2="220"
        stroke="#ef4444"
        stroke-width="8"
    />

    <line
        x1="160"
        y1="250"
        x2="200"
        y2="250"
        stroke="#ef4444"
        stroke-width="5"
    />

    <line
        x1="180"
        y1="220"
        x2="180"
        y2="300"
        stroke="#334155"
        stroke-width="6"
    />

    <text
        x="105"
        y="285"
        font-family="Arial"
        font-size="20"
        fill="#b91c1c"
    >
        Battery
    </text>

    <!-- BULB -->

    <circle
        cx="760"
        cy="260"
        r="45"
        fill="#fde68a"
        stroke="#f59e0b"
        stroke-width="7"
    >

        <animate
            attributeName="fill"
            values="#fde68a;#facc15;#fde68a"
            dur="1s"
            repeatCount="indefinite"
        />

    </circle>

    <path
        d="M735 255 Q760 220 785 255"
        fill="none"
        stroke="#92400e"
        stroke-width="5"
    />

    <path
        d="M735 265 Q760 300 785 265"
        fill="none"
        stroke="#92400e"
        stroke-width="5"
    />

    <text
        x="725"
        y="330"
        font-family="Arial"
        font-size="20"
        fill="#92400e"
    >
        Bulb
    </text>

    <!-- MOVING CHARGE -->

    <circle
        r="12"
        fill="#4f46e5"
    >

        <animateMotion
            dur="4s"
            repeatCount="indefinite"
            path="
                M180 120
                L760 120
                L760 350
                L180 350
                L180 120
            "
        />

    </circle>

    <text
        x="330"
        y="410"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#4338ca"
    >
        Closed circuit → current can flow
    </text>

</svg>
"""


# =========================================================
# SVG 2 — OHM'S LAW
# =========================================================

ohm_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 450">

    <rect
        width="1000"
        height="450"
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
        Ohm's Law — Voltage, Current &amp; Resistance
    </text>

    <!-- VOLTAGE -->

    <rect
        x="80"
        y="130"
        width="230"
        height="150"
        rx="22"
        fill="#dbeafe"
        stroke="#2563eb"
        stroke-width="4"
    />

    <text
        x="195"
        y="185"
        text-anchor="middle"
        font-family="Arial"
        font-size="28"
        font-weight="700"
        fill="#1d4ed8"
    >
        VOLTAGE
    </text>

    <text
        x="195"
        y="230"
        text-anchor="middle"
        font-family="Arial"
        font-size="44"
        font-weight="700"
        fill="#1d4ed8"
    >
        V
    </text>

    <!-- CURRENT -->

    <rect
        x="385"
        y="130"
        width="230"
        height="150"
        rx="22"
        fill="#dcfce7"
        stroke="#16a34a"
        stroke-width="4"
    />

    <text
        x="500"
        y="185"
        text-anchor="middle"
        font-family="Arial"
        font-size="28"
        font-weight="700"
        fill="#15803d"
    >
        CURRENT
    </text>

    <text
        x="500"
        y="230"
        text-anchor="middle"
        font-family="Arial"
        font-size="44"
        font-weight="700"
        fill="#15803d"
    >
        I
    </text>

    <!-- RESISTANCE -->

    <rect
        x="690"
        y="130"
        width="230"
        height="150"
        rx="22"
        fill="#fee2e2"
        stroke="#dc2626"
        stroke-width="4"
    />

    <text
        x="805"
        y="185"
        text-anchor="middle"
        font-family="Arial"
        font-size="25"
        font-weight="700"
        fill="#b91c1c"
    >
        RESISTANCE
    </text>

    <text
        x="805"
        y="230"
        text-anchor="middle"
        font-family="Arial"
        font-size="44"
        font-weight="700"
        fill="#b91c1c"
    >
        R
    </text>

    <text
        x="355"
        y="365"
        font-family="Arial"
        font-size="40"
        font-weight="700"
        fill="#172033"
    >
        V = I × R
    </text>

    <text
        x="280"
        y="410"
        font-family="Arial"
        font-size="21"
        fill="#172033"
    >
        More voltage pushes more current; resistance opposes current
    </text>

</svg>
"""


# =========================================================
# SVG 3 — SERIES VS PARALLEL
# =========================================================

series_parallel_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 470">

    <rect
        width="1000"
        height="470"
        rx="28"
        fill="#fff7ed"
    />

    <text
        x="45"
        y="55"
        font-family="Arial"
        font-size="32"
        font-weight="700"
        fill="#172033"
    >
        Series vs Parallel Circuits
    </text>

    <!-- SERIES SIDE -->

    <text
        x="200"
        y="105"
        font-family="Arial"
        font-size="25"
        font-weight="700"
        fill="#7c3aed"
    >
        SERIES
    </text>

    <path
        d="M80 200 L430 200"
        stroke="#334155"
        stroke-width="7"
        fill="none"
    />

    <circle
        cx="190"
        cy="200"
        r="35"
        fill="#fde68a"
        stroke="#f59e0b"
        stroke-width="5"
    />

    <circle
        cx="330"
        cy="200"
        r="35"
        fill="#fde68a"
        stroke="#f59e0b"
        stroke-width="5"
    />

    <text
        x="95"
        y="300"
        font-family="Arial"
        font-size="19"
        fill="#172033"
    >
        One path for current
    </text>

    <text
        x="95"
        y="335"
        font-family="Arial"
        font-size="19"
        fill="#172033"
    >
        Same current through components
    </text>

    <!-- PARALLEL SIDE -->

    <text
        x="685"
        y="105"
        font-family="Arial"
        font-size="25"
        font-weight="700"
        fill="#15803d"
    >
        PARALLEL
    </text>

    <path
        d="M560 150 L560 300"
        stroke="#334155"
        stroke-width="7"
    />

    <path
        d="M900 150 L900 300"
        stroke="#334155"
        stroke-width="7"
    />

    <path
        d="M560 165 L900 165"
        stroke="#334155"
        stroke-width="7"
    />

    <path
        d="M560 285 L900 285"
        stroke="#334155"
        stroke-width="7"
    />

    <circle
        cx="730"
        cy="165"
        r="33"
        fill="#fde68a"
        stroke="#f59e0b"
        stroke-width="5"
    />

    <circle
        cx="730"
        cy="285"
        r="33"
        fill="#fde68a"
        stroke="#f59e0b"
        stroke-width="5"
    />

    <text
        x="615"
        y="370"
        font-family="Arial"
        font-size="19"
        fill="#172033"
    >
        Multiple paths for current
    </text>

    <text
        x="615"
        y="405"
        font-family="Arial"
        font-size="19"
        fill="#172033"
    >
        Same voltage across branches
    </text>

</svg>
"""


# =========================================================
# SAVE VISUALS
# =========================================================

(
    MEDIA_DIR
    / "simple_circuit.svg"
).write_text(
    circuit_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "ohms_law.svg"
).write_text(
    ohm_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "series_parallel.svg"
).write_text(
    series_parallel_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # TOPIC 7
    # =====================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == 7
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 7 not found."
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
                "Electricity & Electric Circuits",

            subtitle=
                "Understand current, voltage, resistance and how electrical circuits deliver energy.",

            introduction=
                "Your phone charger, lights, laptop and almost every electronic device depend on electric circuits. Let us follow the path of electrical charge and understand what makes a circuit work.",

            pdf_url=None,

            version=1,

            is_active=True
        )


        db.add(note)

        db.commit()

        db.refresh(note)


    else:

        note.title = (
            "Electricity & Electric Circuits"
        )

        note.subtitle = (
            "Understand current, voltage, resistance and how electrical circuits deliver energy."
        )

        note.introduction = (
            "Your phone charger, lights, laptop and almost every electronic device depend on electric circuits. Let us follow the path of electrical charge and understand what makes a circuit work."
        )

        db.commit()


    # =====================================================
    # REMOVE OLD SECTIONS
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
        # INTRO STORY
        # -------------------------------------------------

        {
            "order": 10,

            "type": "story",

            "heading":
                "What Happens When You Switch On a Bulb?",

            "body": """
Imagine a simple circuit containing:

• A battery
• Connecting wires
• A bulb
• A switch


When the switch is OPEN:

The conducting path is broken.

Current cannot flow continuously.

The bulb remains OFF.


When the switch is CLOSED:

A complete conducting path exists.

Electric current can flow through the circuit.

The bulb receives electrical energy
and converts it mainly into:

• Light
• Heat


WHAT IS AN ELECTRIC CIRCUIT?

An electric circuit is a complete path
through which electric charge can move.


THE BASIC CONNECTION

Battery
→ provides electrical potential difference

Wires
→ provide conducting path

Current
→ charge flow

Bulb
→ converts electrical energy


ONE-LINE TAKEAWAY

A closed conducting path is required
for continuous electric current.
""",

            "media_url":
                "/uploads/notes/physics/topic_7/simple_circuit.svg",

            "media_type":
                "svg",

            "caption":
                "In a closed circuit, charge can move continuously through the conducting path.",

            "alt_text":
                "Animated battery and bulb circuit showing charge moving around a closed circuit."
        },


        # -------------------------------------------------
        # CURRENT
        # -------------------------------------------------

        {
            "order": 20,

            "type": "definition",

            "heading":
                "Electric Current — Flow of Charge",

            "body": """
Electric current describes
the rate of flow of electric charge.


FORMULA

I = Q / t


Where:

I = Current

Q = Electric charge

t = Time


SI UNIT

Ampere

Symbol:

A


EXAMPLE

Suppose 10 coulombs of charge
passes through a conductor in 2 seconds.

I = Q / t

I = 10 / 2

I = 5 A


CONVENTIONAL CURRENT

By convention,
current direction is taken from:

Positive terminal
→ Negative terminal

through the external circuit.


IMPORTANT

The actual electrons in a metallic conductor
move in the opposite direction
to conventional current.


ONE-LINE TAKEAWAY

Current tells us how much electric charge
passes a point each second.
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
                "Quick Check 1 — Electric Current",

            "body":
                "Use I = Q / t.",

            "interactive": {

                "question":
                    "12 coulombs of charge pass through a wire in 3 seconds. What is the current?",

                "options": [
                    "4 A",
                    "9 A",
                    "15 A",
                    "36 A"
                ],

                "answer":
                    "4 A",

                "explanation":
                    "Current I = Q / t = 12 / 3 = 4 A."
            }
        },


        # -------------------------------------------------
        # VOLTAGE
        # -------------------------------------------------

        {
            "order": 30,

            "type": "real_world",

            "heading":
                "Voltage — What Pushes Charge Through a Circuit?",

            "body": """
Current needs a reason to flow.

A battery creates a difference
in electric potential between its terminals.

This is called:

POTENTIAL DIFFERENCE

or

VOLTAGE.


Voltage represents energy transferred
per unit charge.


FORMULA

V = W / Q


Where:

V = Voltage

W = Energy transferred

Q = Charge


SI UNIT

Volt

Symbol:

V


A SIMPLE WAY TO THINK ABOUT IT

Voltage is like the electrical push
that encourages charge to move.


BATTERY EXAMPLE

A battery converts chemical energy
into electrical energy.

That energy difference helps drive current
around a closed circuit.


IMPORTANT

Voltage is not current.

Voltage helps drive charge.

Current is the rate at which charge flows.


ONE-LINE TAKEAWAY

Voltage provides the electrical potential difference
that can drive current.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # RESISTANCE + OHM
        # -------------------------------------------------

        {
            "order": 40,

            "type": "animation",

            "heading":
                "Resistance and Ohm's Law",

            "body": """
Materials oppose the motion of electric charge
by different amounts.

This opposition is called RESISTANCE.


Symbol:

R


SI Unit:

Ohm

Symbol:

Ω


OHM'S LAW

For many conductors under suitable conditions:

V = I × R


This can also be written as:

I = V / R


or:

R = V / I


WHAT DOES THIS MEAN?


IF RESISTANCE STAYS CONSTANT:

More Voltage
→ More Current


IF VOLTAGE STAYS CONSTANT:

More Resistance
→ Less Current


EXAMPLE

Voltage:

V = 12 V


Resistance:

R = 4 Ω


Current:

I = V / R

I = 12 / 4

I = 3 A


REAL-WORLD CONNECTION

Resistance helps control current
inside electrical and electronic circuits.


ONE-LINE TAKEAWAY

Voltage drives current,
while resistance opposes it.
""",

            "media_url":
                "/uploads/notes/physics/topic_7/ohms_law.svg",

            "media_type":
                "svg",

            "caption":
                "Ohm's Law connects voltage, current and resistance through V = IR.",

            "alt_text":
                "Visual relationship between voltage, current and resistance."
        },


        # -------------------------------------------------
        # CHECK 2
        # -------------------------------------------------

        {
            "order": 45,

            "type": "checkpoint",

            "heading":
                "Quick Check 2 — Ohm's Law",

            "body":
                "Use I = V / R.",

            "interactive": {

                "question":
                    "A 12 V battery is connected across a 4 Ω resistor. What current flows?",

                "options": [
                    "3 A",
                    "8 A",
                    "16 A",
                    "48 A"
                ],

                "answer":
                    "3 A",

                "explanation":
                    "Using Ohm's Law, I = V / R = 12 / 4 = 3 A."
            }
        },


        # -------------------------------------------------
        # SERIES CIRCUITS
        # -------------------------------------------------

        {
            "order": 50,

            "type": "definition",

            "heading":
                "Series Circuits — One Path for Current",

            "body": """
In a SERIES circuit,
components are connected one after another.

There is only ONE main path
for current.


IMPORTANT SERIES RULES


CURRENT

The same current flows
through each component in series.


VOLTAGE

The supply voltage is shared
across the components.


RESISTANCE

For resistors in series:

R_total
=
R₁ + R₂ + R₃ + ...


EXAMPLE

Two resistors:

R₁ = 2 Ω

R₂ = 4 Ω


Total resistance:

R_total = 2 + 4

R_total = 6 Ω


REAL-WORLD IDEA

If one component breaks
and opens the path,
current through the whole series path can stop.


ONE-LINE TAKEAWAY

Series circuits provide one current path,
and their resistances add together.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # PARALLEL
        # -------------------------------------------------

        {
            "order": 60,

            "type": "real_world",

            "heading":
                "Parallel Circuits — Multiple Paths",

            "body": """
In a PARALLEL circuit,
components are connected across
the same two main points.

This creates multiple paths
for current.


IMPORTANT PARALLEL RULES


VOLTAGE

The same voltage appears
across each parallel branch.


CURRENT

The total current splits
between the branches.


TOTAL CURRENT

I_total
=
I₁ + I₂ + I₃ + ...


WHY HOMES USE PARALLEL CONNECTIONS

Household electrical devices are generally connected
in parallel.

Why?

Because each appliance can receive
the supply voltage independently.

Also:

One appliance can be switched off
without automatically stopping all the others.


REAL-WORLD EXAMPLE

Imagine:

One room light switched OFF.

The fan in another room
can still operate.


ONE-LINE TAKEAWAY

Parallel circuits give current
multiple independent paths.
""",

            "media_url":
                "/uploads/notes/physics/topic_7/series_parallel.svg",

            "media_type":
                "svg",

            "caption":
                "Series circuits have one path; parallel circuits provide multiple branches.",

            "alt_text":
                "Diagram comparing series and parallel electric circuits."
        },


        # -------------------------------------------------
        # CHECK 3
        # -------------------------------------------------

        {
            "order": 65,

            "type": "checkpoint",

            "heading":
                "Quick Check 3 — Series or Parallel?",

            "body":
                "Think about independent circuit branches.",

            "interactive": {

                "question":
                    "Why are household appliances generally connected in parallel rather than all in one series path?",

                "options": [
                    "Each appliance can operate independently across the supply",
                    "Parallel circuits contain no current",
                    "Series circuits always use zero voltage",
                    "Parallel circuits eliminate resistance completely"
                ],

                "answer":
                    "Each appliance can operate independently across the supply",

                "explanation":
                    "In a parallel connection, each branch receives the supply voltage and individual appliances can be switched independently."
            }
        },


        # -------------------------------------------------
        # POWER
        # -------------------------------------------------

        {
            "order": 70,

            "type": "application",

            "heading":
                "Electrical Power — How Fast Is Electrical Energy Used?",

            "body": """
Electrical power tells us
the rate at which electrical energy
is transferred or converted.


FORMULA

P = V × I


Where:

P = Power

V = Voltage

I = Current


SI UNIT

Watt

W


EXAMPLE

A device operates at:

V = 12 V

I = 2 A


Power:

P = 12 × 2

P = 24 W


OTHER USEFUL FORMS

Using Ohm's Law:

P = I²R

and

P = V² / R


REAL-WORLD EXAMPLES

A higher-power heater converts electrical energy
into heat more rapidly.

A motor with greater electrical input power
can potentially perform mechanical work
at a greater rate,
depending on efficiency.


ENERGY CONNECTION

Electrical energy used:

E = P × t


ONE-LINE TAKEAWAY

Electrical power measures how quickly
electrical energy is transferred.
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
            "order": 75,

            "type": "checkpoint",

            "heading":
                "Quick Check 4 — Electrical Power",

            "body":
                "Use P = VI.",

            "interactive": {

                "question":
                    "A device operates at 10 V and draws 3 A. What electrical power does it use?",

                "options": [
                    "3.3 W",
                    "7 W",
                    "13 W",
                    "30 W"
                ],

                "answer":
                    "30 W",

                "explanation":
                    "Electrical power P = V × I = 10 × 3 = 30 W."
            }
        },


        # -------------------------------------------------
        # APPLICATIONS
        # -------------------------------------------------

        {
            "order": 80,

            "type": "application",

            "heading":
                "Where Do We Use Electric Circuits?",

            "body": """
📱 SMARTPHONES

Complex circuits distribute power
to processors, displays, cameras and sensors.


💻 COMPUTERS

Electrical circuits control:

• Processing
• Memory
• Communication
• Power delivery


🤖 ROBOTS

Robots use electrical circuits for:

• Motors
• Sensors
• Controllers
• Batteries
• Communication modules


🏠 HOMES

Parallel circuits distribute electrical power
to lights and appliances.


🚗 ELECTRIC VEHICLES

Battery packs supply electrical energy
to power electronics and electric motors.


☀️ SOLAR SYSTEMS

Solar panels generate electrical energy.

Converters and circuits manage
how that energy is stored and used.


🏥 MEDICAL DEVICES

Electronic circuits are essential
in monitoring and diagnostic equipment.


Understanding voltage, current and resistance
is therefore fundamental to modern technology.
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
            "order": 90,

            "type": "summary",

            "heading":
                "What Should You Remember?",

            "body": """
ELECTRIC CIRCUIT

A complete conducting path
for charge movement.


CURRENT

Rate of charge flow.

I = Q / t

Unit = Ampere


VOLTAGE

Electrical potential difference.

Helps drive current.

Unit = Volt


RESISTANCE

Opposition to current.

Unit = Ohm


OHM'S LAW

V = IR


SERIES CIRCUIT

One current path.

Same current through components.

R_total = R₁ + R₂ + ...


PARALLEL CIRCUIT

Multiple current paths.

Same voltage across branches.

I_total = I₁ + I₂ + ...


ELECTRICAL POWER

P = VI

Unit = Watt


FINAL CONNECTION

Battery
→ provides potential difference

Voltage
→ drives charge

Charge flow
→ current

Resistance
→ opposes current

V, I and R
→ connected by Ohm's Law

Electrical energy transfer rate
→ power


Electric circuits are the foundation
of almost every modern electronic system.
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
    print(" TOPIC 7 RICH NOTES CREATED SUCCESSFULLY")
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
        / "simple_circuit.svg"
    )

    print(
        MEDIA_DIR
        / "ohms_law.svg"
    )

    print(
        MEDIA_DIR
        / "series_parallel.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 7 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()