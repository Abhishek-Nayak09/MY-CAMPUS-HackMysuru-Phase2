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
    / "topic_1"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — MORNING PHYSICS STORY
# =========================================================

morning_svg = """
<svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 1000 420"
>

    <defs>

        <linearGradient
            id="sky"
            x1="0"
            y1="0"
            x2="1"
            y2="1"
        >

            <stop
                offset="0%"
                stop-color="#dbeafe"
            />

            <stop
                offset="100%"
                stop-color="#ede9fe"
            />

        </linearGradient>

    </defs>


    <rect
        width="1000"
        height="420"
        rx="28"
        fill="url(#sky)"
    />


    <text
        x="50"
        y="65"
        font-size="34"
        font-family="Arial"
        font-weight="700"
        fill="#172033"
    >
        A Morning Full of Physics
    </text>


    <!-- PHONE -->

    <g>

        <rect
            x="80"
            y="135"
            width="115"
            height="190"
            rx="20"
            fill="#111827"
        />

        <rect
            x="95"
            y="155"
            width="85"
            height="125"
            rx="10"
            fill="#818cf8"
        />

        <text
            x="137"
            y="225"
            font-size="38"
            text-anchor="middle"
        >
            ⏰
        </text>

        <text
            x="137"
            y="360"
            font-size="20"
            text-anchor="middle"
            fill="#172033"
        >
            Sound Waves
        </text>

    </g>


    <!-- WALKING -->

    <g>

        <circle
            cx="375"
            cy="180"
            r="33"
            fill="#f59e0b"
        />

        <line
            x1="375"
            y1="212"
            x2="375"
            y2="280"
            stroke="#172033"
            stroke-width="12"
            stroke-linecap="round"
        />

        <line
            x1="375"
            y1="235"
            x2="330"
            y2="265"
            stroke="#172033"
            stroke-width="10"
            stroke-linecap="round"
        />

        <line
            x1="375"
            y1="235"
            x2="420"
            y2="255"
            stroke="#172033"
            stroke-width="10"
            stroke-linecap="round"
        />

        <line
            x1="375"
            y1="280"
            x2="340"
            y2="330"
            stroke="#172033"
            stroke-width="10"
            stroke-linecap="round"
        />

        <line
            x1="375"
            y1="280"
            x2="420"
            y2="320"
            stroke="#172033"
            stroke-width="10"
            stroke-linecap="round"
        />

        <text
            x="375"
            y="360"
            font-size="20"
            text-anchor="middle"
            fill="#172033"
        >
            Friction
        </text>

    </g>


    <!-- CAR -->

    <g id="car">

        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0;45 0;0 0"
            dur="3s"
            repeatCount="indefinite"
        />

        <rect
            x="585"
            y="215"
            width="210"
            height="75"
            rx="25"
            fill="#4f46e5"
        />

        <path
            d="M630 215 L675 165 L735 165 L775 215"
            fill="#6366f1"
        />

        <circle
            cx="635"
            cy="295"
            r="28"
            fill="#111827"
        />

        <circle
            cx="750"
            cy="295"
            r="28"
            fill="#111827"
        />

    </g>


    <text
        x="690"
        y="360"
        font-size="20"
        text-anchor="middle"
        fill="#172033"
    >
        Motion &amp; Force
    </text>


    <!-- SUN / LIGHT -->

    <circle
        cx="885"
        cy="145"
        r="48"
        fill="#fbbf24"
    >

        <animate
            attributeName="r"
            values="43;52;43"
            dur="2s"
            repeatCount="indefinite"
        />

    </circle>


    <text
        x="885"
        y="230"
        font-size="20"
        text-anchor="middle"
        fill="#172033"
    >
        Light &amp; Energy
    </text>

</svg>
"""


# =========================================================
# SVG 2 — FOOTBALL PHYSICS
# =========================================================

football_svg = """
<svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 1000 420"
>

    <rect
        width="1000"
        height="420"
        rx="28"
        fill="#ecfdf5"
    />


    <text
        x="50"
        y="60"
        font-size="32"
        font-family="Arial"
        font-weight="700"
        fill="#172033"
    >
        Physics of a Football Kick
    </text>


    <path
        d="M120 320 Q450 70 800 285"
        fill="none"
        stroke="#6366f1"
        stroke-width="5"
        stroke-dasharray="12 12"
    />


    <circle
        r="28"
        fill="#ffffff"
        stroke="#111827"
        stroke-width="4"
    >

        <animateMotion
            dur="4s"
            repeatCount="indefinite"
            path="M120 320 Q450 70 800 285"
        />

    </circle>


    <!-- FORCE -->

    <line
        x1="125"
        y1="305"
        x2="245"
        y2="245"
        stroke="#dc2626"
        stroke-width="8"
    />

    <polygon
        points="245,245 220,245 232,265"
        fill="#dc2626"
    />


    <text
        x="185"
        y="225"
        font-size="20"
        fill="#dc2626"
    >
        Force
    </text>


    <!-- GRAVITY -->

    <line
        x1="500"
        y1="135"
        x2="500"
        y2="255"
        stroke="#2563eb"
        stroke-width="8"
    />

    <polygon
        points="500,270 485,242 515,242"
        fill="#2563eb"
    />


    <text
        x="520"
        y="205"
        font-size="20"
        fill="#2563eb"
    >
        Gravity
    </text>


    <text
        x="120"
        y="380"
        font-size="19"
        fill="#172033"
    >
        Kick → Force → Motion → Gravity → Curved Path
    </text>

</svg>
"""


# =========================================================
# SVG 3 — ROCKET ACTION / REACTION
# =========================================================

rocket_svg = """
<svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 1000 430"
>

    <rect
        width="1000"
        height="430"
        rx="28"
        fill="#111827"
    />


    <circle
        cx="90"
        cy="85"
        r="3"
        fill="white"
    />

    <circle
        cx="170"
        cy="160"
        r="4"
        fill="white"
    />

    <circle
        cx="850"
        cy="110"
        r="4"
        fill="white"
    />

    <circle
        cx="760"
        cy="230"
        r="3"
        fill="white"
    />


    <text
        x="50"
        y="60"
        font-size="32"
        font-family="Arial"
        font-weight="700"
        fill="white"
    >
        Newton's Third Law in a Rocket
    </text>


    <g id="rocket">

        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 20;0 -20;0 20"
            dur="2.5s"
            repeatCount="indefinite"
        />


        <path
            d="M500 115
               C455 165 450 235 500 300
               C550 235 545 165 500 115"
            fill="#e5e7eb"
        />


        <circle
            cx="500"
            cy="195"
            r="24"
            fill="#60a5fa"
        />


        <polygon
            points="470,270 445,320 485,300"
            fill="#ef4444"
        />


        <polygon
            points="530,270 555,320 515,300"
            fill="#ef4444"
        />


        <polygon
            points="480,300 500,385 520,300"
            fill="#f59e0b"
        >

            <animate
                attributeName="points"
                values="
                    480,300 500,365 520,300;
                    480,300 500,400 520,300;
                    480,300 500,365 520,300
                "
                dur="0.5s"
                repeatCount="indefinite"
            />

        </polygon>

    </g>


    <line
        x1="650"
        y1="285"
        x2="650"
        y2="155"
        stroke="#22c55e"
        stroke-width="8"
    />


    <polygon
        points="650,140 635,170 665,170"
        fill="#22c55e"
    />


    <text
        x="680"
        y="210"
        font-size="20"
        fill="#86efac"
    >
        Reaction: Rocket moves UP
    </text>


    <line
        x1="350"
        y1="180"
        x2="350"
        y2="325"
        stroke="#f97316"
        stroke-width="8"
    />


    <polygon
        points="350,340 335,310 365,310"
        fill="#f97316"
    />


    <text
        x="70"
        y="280"
        font-size="20"
        fill="#fdba74"
    >
        Action: Exhaust gases pushed DOWN
    </text>

</svg>
"""


# =========================================================
# SAVE SVG FILES
# =========================================================

(
    MEDIA_DIR
    / "morning_physics.svg"
).write_text(
    morning_svg,
    encoding="utf-8"
)


(
    MEDIA_DIR
    / "football_physics.svg"
).write_text(
    football_svg,
    encoding="utf-8"
)


(
    MEDIA_DIR
    / "rocket_physics.svg"
).write_text(
    rocket_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =========================================================
    # FIND TOPIC
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

        raise Exception(
            "Topic 1 not found."
        )


    # =========================================================
    # FIND / CREATE NOTE
    # =========================================================

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
                "Why Physics? — Discover Physics Around You",

            subtitle=
                "A story-driven introduction to the Physics hidden in everyday life.",

            introduction=
                "Before learning equations, let us first discover why Physics matters and where we experience it every day.",

            pdf_url=None,

            version=1,

            is_active=True
        )


        db.add(note)

        db.commit()

        db.refresh(note)


    else:

        note.title = (
            "Why Physics? — Discover Physics Around You"
        )

        note.subtitle = (
            "A story-driven introduction to the Physics hidden in everyday life."
        )

        note.introduction = (
            "Before learning equations, let us first discover why Physics matters and where we experience it every day."
        )


        db.commit()


    # =========================================================
    # REMOVE OLD DEMO SECTIONS
    # =========================================================

    (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id
        )
        .delete()
    )


    # =========================================================
    # RICH NOTE SECTIONS
    # =========================================================

    sections = [

        # -----------------------------------------------------
        # STORY
        # -----------------------------------------------------

        {
            "section_order": 1,

            "section_type": "story",

            "heading":
                "A Morning Full of Physics",

            "body": """
Imagine your normal morning.

Your phone alarm rings.

You hear it because vibrations from the speaker
travel through air as SOUND WAVES.

You get out of bed and start walking.

Why don't your feet simply slide backward?

Because FRICTION between your feet and the floor
helps you push against the ground.

You switch on the light.

Electrical energy travels through the circuit
and is converted into light and heat.

Then you travel to college in a car or bus.

Every acceleration, turn and brake involves:

• Force
• Motion
• Friction
• Energy
• Momentum

Before your first class has even started,
you have already experienced Physics many times.
""",

            "media_url":
                "/uploads/notes/physics/topic_1/morning_physics.svg",

            "media_type":
                "svg",

            "caption":
                "From your alarm to your journey to college, Physics is already working around you.",

            "alt_text":
                "Animated illustration showing a phone alarm, a walking person, a moving car and sunlight representing everyday Physics.",

            "interactive_data":
                None
        },


        # -----------------------------------------------------
        # DEFINITION
        # -----------------------------------------------------

        {
            "section_order": 2,

            "section_type": "definition",

            "heading":
                "So, What Exactly Is Physics?",

            "body": """
Physics is the science of understanding how the physical world behaves.

It studies ideas such as:

• Matter — the things around us
• Motion — how objects move
• Force — what changes motion
• Energy — the ability to cause change
• Waves — how sound and signals travel
• Electricity — movement and interaction of electric charge
• Light — how we see and transmit information
• Space and Time — how events and motion are described

The most useful way to think about Physics is:

“Observe what happens → understand why it happens →
predict what will happen next.”

That is why Physics is not simply a collection of formulas.
It is a way of understanding and designing the world.
""",

            "media_url":
                None,

            "media_type":
                None,

            "caption":
                None,

            "alt_text":
                None,

            "interactive_data":
                None
        },


        # -----------------------------------------------------
        # REAL WORLD — FOOTBALL
        # -----------------------------------------------------

        {
            "section_order": 3,

            "section_type": "real_world",

            "heading":
                "Example 1 — What Happens When You Kick a Football?",

            "body": """
Suppose a football is resting on the ground.

Nothing happens until your foot applies a FORCE.

The kick gives the football velocity.

As the ball rises, GRAVITY continuously pulls it downward.

Because the ball has mass and velocity,
it also possesses MOMENTUM.

The beautiful curved path you see in the air
is not random.

It is the result of motion and gravity acting together.

So one simple football kick connects multiple ideas:

Force → Motion → Velocity → Gravity → Momentum

This is exactly how Physics helps us break a real event
into understandable concepts.
""",

            "media_url":
                "/uploads/notes/physics/topic_1/football_physics.svg",

            "media_type":
                "svg",

            "caption":
                "An animated football trajectory showing force and gravity.",

            "alt_text":
                "Football moving along a curved trajectory with force and gravity arrows.",

            "interactive_data":
                None
        },


        # -----------------------------------------------------
        # REAL WORLD COLLECTION
        # -----------------------------------------------------

        {
            "section_order": 4,

            "section_type": "application",

            "heading":
                "Physics Is Hidden Inside the Technology Around You",

            "body": """
🚗 VEHICLES

When a car accelerates:
Force changes its motion.

When the driver brakes:
Friction and braking force reduce its speed.

When a car moves fast:
Its momentum increases.


🌉 BUILDINGS AND BRIDGES

Civil engineers calculate:

• Weight
• Support forces
• Stress
• Balance
• Load distribution

A building remains stable only when the acting forces
are properly understood.


📱 SMARTPHONES

Your phone depends on several Physics principles:

• Electricity powers its circuits.
• Electromagnetic waves carry wireless data.
• Light creates the screen image.
• Sound waves operate the microphone and speaker.
• Semiconductor Physics makes modern processors possible.


🏥 MEDICINE

Doctors use Physics every day.

X-rays help reveal bones.

Ultrasound uses high-frequency sound waves.

MRI uses strong magnetic fields and radio waves.

Physics can literally help doctors see inside the human body.
""",

            "media_url":
                None,

            "media_type":
                None,

            "caption":
                None,

            "alt_text":
                None,

            "interactive_data":
                None
        },


        # -----------------------------------------------------
        # ROCKET ANIMATION
        # -----------------------------------------------------

        {
            "section_order": 5,

            "section_type": "animation",

            "heading":
                "Example 2 — How Can a Rocket Move in Space?",

            "body": """
A rocket engine pushes hot gases downward at high speed.

According to Newton's Third Law:

For every action, there is an equal and opposite reaction.

ACTION:
The rocket pushes exhaust gases downward.

REACTION:
The gases push the rocket upward.

This principle works even when the rocket leaves Earth's atmosphere.

Gravity, momentum and energy also influence the rocket's journey.

The same Physics learned in a classroom is therefore used
to send satellites, spacecraft and astronauts into space.
""",

            "media_url":
                "/uploads/notes/physics/topic_1/rocket_physics.svg",

            "media_type":
                "svg",

            "caption":
                "Animated action-reaction visualization of rocket propulsion.",

            "alt_text":
                "Animated rocket showing exhaust gases moving downward and the rocket moving upward.",

            "interactive_data":
                None
        },


        # -----------------------------------------------------
        # ENGINEERING APPLICATIONS
        # -----------------------------------------------------

        {
            "section_order": 6,

            "section_type": "application",

            "heading":
                "Where Will You Use Physics in Engineering?",

            "body": """
MECHANICAL ENGINEERING

Motion, machines, heat, energy, forces and fluids.


CIVIL ENGINEERING

Structures, materials, loads, forces and stability.


ELECTRICAL ENGINEERING

Voltage, current, electromagnetic fields and power.


ELECTRONICS & COMMUNICATION

Semiconductors, signals, waves, optics and communication.


COMPUTER ENGINEERING

Computer hardware, electronic circuits,
semiconductors, wireless communication and sensors.


AEROSPACE ENGINEERING

Aerodynamics, propulsion, gravity,
fluid flow, energy and orbital mechanics.


Physics provides the foundation upon which
many engineering technologies are built.
""",

            "media_url":
                None,

            "media_type":
                None,

            "caption":
                None,

            "alt_text":
                None,

            "interactive_data":
                None
        },


        # -----------------------------------------------------
        # CHECKPOINT
        # -----------------------------------------------------

        {
            "section_order": 7,

            "section_type": "checkpoint",

            "heading":
                "Quick Check — Can You Spot the Physics?",

            "body":
                "A passenger moves forward when a suddenly moving car stops. Which Physics idea is mainly responsible?",

            "media_url":
                None,

            "media_type":
                None,

            "caption":
                None,

            "alt_text":
                None,

            "interactive_data":
                json.dumps(
                    {
                        "question":
                            "A passenger moves forward when a moving car suddenly stops. Which idea explains this?",

                        "options": [
                            "Inertia",
                            "Reflection",
                            "Magnetism",
                            "Refraction"
                        ],

                        "answer":
                            "Inertia",

                        "explanation":
                            "The passenger's body tends to continue its existing motion. This resistance to a change in motion is called inertia."
                    }
                )
        },


        # -----------------------------------------------------
        # SUMMARY
        # -----------------------------------------------------

        {
            "section_order": 8,

            "section_type": "summary",

            "heading":
                "What Should You Remember?",

            "body": """
Physics is not limited to equations in a textbook.

It explains:

• Why objects move
• Why objects stop
• How energy changes form
• How sound travels
• How electricity powers devices
• How bridges remain stable
• How doctors create medical images
• How phones communicate
• How rockets reach space

The goal of learning Physics is to understand
the rules behind the world around us.

Once you can see those rules in real life,
the equations begin to make much more sense.
""",

            "media_url":
                None,

            "media_type":
                None,

            "caption":
                None,

            "alt_text":
                None,

            "interactive_data":
                None
        }

    ]


    # =========================================================
    # INSERT SECTIONS
    # =========================================================

    for item in sections:

        section = NoteSection(

            note_id=
                note.id,

            section_order=
                item["section_order"],

            section_type=
                item["section_type"],

            heading=
                item["heading"],

            body=
                item["body"],

            media_url=
                item["media_url"],

            media_type=
                item["media_type"],

            caption=
                item["caption"],

            alt_text=
                item["alt_text"],

            interactive_data=
                item["interactive_data"],

            is_active=True
        )


        db.add(section)


    db.commit()


    # =========================================================
    # VERIFY
    # =========================================================

    saved_sections = (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id ==
            note.id
        )
        .order_by(
            NoteSection.section_order
        )
        .all()
    )


    print("")
    print("==========================================")
    print(" TOPIC 1 RICH NOTES CREATED SUCCESSFULLY")
    print("==========================================")
    print("")

    print(
        f"Note: {note.title}"
    )

    print(
        f"Sections: {len(saved_sections)}"
    )

    print("")


    for section in saved_sections:

        print(
            f"{section.section_order}. "
            f"{section.section_type.upper()} "
            f"- {section.heading}"
        )


    print("")


    print("Generated Visual Assets:")

    print(
        MEDIA_DIR
        / "morning_physics.svg"
    )

    print(
        MEDIA_DIR
        / "football_physics.svg"
    )

    print(
        MEDIA_DIR
        / "rocket_physics.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("RICH NOTES SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()