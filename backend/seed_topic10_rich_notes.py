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
    / "topic_10"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — ATOMIC ENERGY LEVELS
# =========================================================

atom_svg = """
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
        Electrons Occupy Discrete Energy Levels
    </text>

    <!-- NUCLEUS -->

    <circle
        cx="500"
        cy="245"
        r="42"
        fill="#ef4444"
    />

    <text
        x="500"
        y="253"
        text-anchor="middle"
        font-family="Arial"
        font-size="20"
        font-weight="700"
        fill="white"
    >
        Nucleus
    </text>

    <!-- ORBITS -->

    <ellipse
        cx="500"
        cy="245"
        rx="140"
        ry="80"
        fill="none"
        stroke="#6366f1"
        stroke-width="4"
    />

    <ellipse
        cx="500"
        cy="245"
        rx="240"
        ry="140"
        fill="none"
        stroke="#8b5cf6"
        stroke-width="4"
    />

    <!-- ELECTRON -->

    <circle
        r="14"
        fill="#2563eb"
    >
        <animateMotion
            dur="3s"
            repeatCount="indefinite"
            path="M640 245
                  A140 80 0 1 1 360 245
                  A140 80 0 1 1 640 245"
        />
    </circle>

    <circle
        r="14"
        fill="#16a34a"
    >
        <animateMotion
            dur="5s"
            repeatCount="indefinite"
            path="M740 245
                  A240 140 0 1 1 260 245
                  A240 140 0 1 1 740 245"
        />
    </circle>

    <text
        x="255"
        y="425"
        font-family="Arial"
        font-size="23"
        font-weight="700"
        fill="#4338ca"
    >
        Electrons can change energy levels by absorbing or emitting energy
    </text>

</svg>
"""


# =========================================================
# SVG 2 — PHOTOELECTRIC EFFECT
# =========================================================

photoelectric_svg = """
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
        Photoelectric Effect
    </text>

    <!-- LIGHT -->

    <path
        d="M100 160
           Q140 120 180 160
           T260 160
           T340 160"
        fill="none"
        stroke="#f59e0b"
        stroke-width="8"
    />

    <polygon
        points="350,160 320,142 320,178"
        fill="#f59e0b"
    />

    <text
        x="120"
        y="120"
        font-family="Arial"
        font-size="21"
        fill="#b45309"
    >
        Incoming photons
    </text>

    <!-- METAL -->

    <rect
        x="430"
        y="115"
        width="90"
        height="250"
        rx="12"
        fill="#64748b"
    />

    <text
        x="455"
        y="405"
        font-family="Arial"
        font-size="20"
        fill="#475569"
    >
        Metal
    </text>

    <!-- ELECTRONS -->

    <circle cx="470" cy="180" r="12" fill="#2563eb"/>
    <circle cx="470" cy="245" r="12" fill="#2563eb"/>
    <circle cx="470" cy="310" r="12" fill="#2563eb"/>

    <!-- EJECTED ELECTRON -->

    <circle
        r="14"
        fill="#2563eb"
    >
        <animateMotion
            dur="2.5s"
            repeatCount="indefinite"
            path="M500 180 Q650 100 830 145"
        />
    </circle>

    <line
        x1="520"
        y1="180"
        x2="820"
        y2="140"
        stroke="#2563eb"
        stroke-width="4"
        stroke-dasharray="12 10"
    />

    <text
        x="645"
        y="105"
        font-family="Arial"
        font-size="21"
        fill="#1d4ed8"
    >
        Electron emitted
    </text>

    <text
        x="580"
        y="330"
        font-family="Arial"
        font-size="23"
        font-weight="700"
        fill="#ea580c"
    >
        Photon energy can free an electron
    </text>

</svg>
"""


# =========================================================
# SVG 3 — MASS ENERGY
# =========================================================

mass_energy_svg = """
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
        Mass and Energy Are Related
    </text>

    <rect
        x="100"
        y="140"
        width="280"
        height="180"
        rx="24"
        fill="#ffffff"
        stroke="#86efac"
        stroke-width="4"
    />

    <text
        x="240"
        y="205"
        text-anchor="middle"
        font-family="Arial"
        font-size="28"
        font-weight="700"
        fill="#15803d"
    >
        MASS
    </text>

    <text
        x="240"
        y="270"
        text-anchor="middle"
        font-family="Arial"
        font-size="44"
        font-weight="700"
        fill="#166534"
    >
        m
    </text>

    <line
        x1="400"
        y1="230"
        x2="590"
        y2="230"
        stroke="#7c3aed"
        stroke-width="8"
    />

    <polygon
        points="610,230 575,208 575,252"
        fill="#7c3aed"
    />

    <rect
        x="630"
        y="140"
        width="280"
        height="180"
        rx="24"
        fill="#ffffff"
        stroke="#86efac"
        stroke-width="4"
    />

    <text
        x="770"
        y="205"
        text-anchor="middle"
        font-family="Arial"
        font-size="28"
        font-weight="700"
        fill="#15803d"
    >
        ENERGY
    </text>

    <text
        x="770"
        y="270"
        text-anchor="middle"
        font-family="Arial"
        font-size="44"
        font-weight="700"
        fill="#166534"
    >
        E
    </text>

    <text
        x="360"
        y="395"
        font-family="Arial"
        font-size="38"
        font-weight="700"
        fill="#172033"
    >
        E = mc²
    </text>

</svg>
"""


# =========================================================
# SAVE VISUALS
# =========================================================

(
    MEDIA_DIR
    / "atomic_energy_levels.svg"
).write_text(
    atom_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "photoelectric_effect.svg"
).write_text(
    photoelectric_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "mass_energy.svg"
).write_text(
    mass_energy_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # TOPIC 10
    # =====================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == 10
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 10 not found."
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
                "Modern Physics",

            subtitle=
                "Explore atoms, photons, quantum ideas, radioactivity and the physics behind modern technology.",

            introduction=
                "Classical Physics explains much of everyday motion, forces, waves and electricity. But atoms, light and extremely small particles behave in ways that require new ideas. Modern Physics helps us understand this microscopic world.",

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
            "Modern Physics"
        )

        note.subtitle = (
            "Explore atoms, photons, quantum ideas, radioactivity and the physics behind modern technology."
        )

        note.introduction = (
            "Classical Physics explains much of everyday motion, forces, waves and electricity. But atoms, light and extremely small particles behave in ways that require new ideas. Modern Physics helps us understand this microscopic world."
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
        # INTRO
        # -------------------------------------------------

        {
            "order": 10,

            "type": "story",

            "heading":
                "Why Did Physics Need New Ideas?",

            "body": """
Classical Physics works extremely well
for many everyday situations.

It explains:

• Cars moving
• Falling objects
• Machines
• Waves
• Electric circuits
• Magnetism


But scientists discovered something interesting.

When they studied:

• Atoms
• Electrons
• Light
• Radioactivity
• Very high speeds

classical ideas alone were not enough.


This led to:

MODERN PHYSICS


Modern Physics includes ideas from:

• Quantum Physics
• Atomic Physics
• Nuclear Physics
• Relativity
• Particle Physics


WHY IS IT IMPORTANT?

Modern Physics explains technologies such as:

• Semiconductors
• Computers
• Smartphones
• Lasers
• Solar cells
• Medical imaging
• Nuclear energy
• GPS


ONE-LINE TAKEAWAY

Modern Physics explains nature
at atomic scales and extreme conditions.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # ATOM
        # -------------------------------------------------

        {
            "order": 20,

            "type": "animation",

            "heading":
                "Atoms and Quantized Energy Levels",

            "body": """
Matter is made of atoms.

A simplified atom contains:

NUCLEUS

Containing:

• Protons
• Neutrons


ELECTRONS

Located around the nucleus.


MODERN IDEA

Electrons cannot possess
just any arbitrary atomic energy.

They occupy allowed energy states.


These are called:

ENERGY LEVELS.


QUANTIZED ENERGY

The word QUANTIZED means:

Only certain discrete values
are allowed.


ELECTRON TRANSITION

An electron can move
from a lower energy level
to a higher level by absorbing energy.


Lower Level
→ Absorb Energy
→ Higher Level


An electron can also move
from a higher level
to a lower level.


Higher Level
→ Lower Level
→ Energy emitted


Often that energy can be emitted
as a photon of light.


ONE-LINE TAKEAWAY

Atomic energy comes in discrete allowed levels.
""",

            "media_url":
                "/uploads/notes/physics/topic_10/atomic_energy_levels.svg",

            "media_type":
                "svg",

            "caption":
                "Electrons can change between allowed atomic energy states by absorbing or emitting energy.",

            "alt_text":
                "Animated simplified atom showing electrons in different energy levels."
        },


        # -------------------------------------------------
        # CHECK 1
        # -------------------------------------------------

        {
            "order": 25,

            "type": "checkpoint",

            "heading":
                "Quick Check 1 — Atomic Energy",

            "body":
                "Remember what quantized means.",

            "interactive": {

                "question":
                    "What does it mean when atomic energy levels are described as quantized?",

                "options": [
                    "Only certain discrete energy values are allowed",
                    "Every possible energy value is always allowed",
                    "Electrons have zero energy",
                    "Atoms cannot absorb energy"
                ],

                "answer":
                    "Only certain discrete energy values are allowed",

                "explanation":
                    "Quantization means the electron can occupy specific allowed energy states rather than every possible intermediate energy value."
            }
        },


        # -------------------------------------------------
        # PHOTONS
        # -------------------------------------------------

        {
            "order": 30,

            "type": "definition",

            "heading":
                "Photons — Light Comes in Energy Packets",

            "body": """
Classically,
light behaves like a wave.

Modern Physics revealed
that light also behaves as if
its energy comes in discrete packets.


These packets are called:

PHOTONS.


PHOTON ENERGY

Photon energy depends on frequency.


FORMULA

E = h × f


Where:

E = Photon energy

h = Planck's constant

f = Frequency


IMPORTANT CONNECTION

Higher frequency
→ Higher photon energy


Lower frequency
→ Lower photon energy


CONNECT WITH WAVES

Earlier we learned:

Frequency determines
how rapidly a wave oscillates.


Modern Physics adds:

For light,
frequency also determines
the energy of each photon.


EXAMPLE

Ultraviolet light has
a higher frequency than visible red light.

Therefore ultraviolet photons
carry more energy than red photons.


ONE-LINE TAKEAWAY

Light energy is carried in packets called photons.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # PHOTOELECTRIC
        # -------------------------------------------------

        {
            "order": 40,

            "type": "animation",

            "heading":
                "Photoelectric Effect — Light Can Release Electrons",

            "body": """
When light strikes certain materials,
electrons can be emitted
from the surface.

This is called:

THE PHOTOELECTRIC EFFECT.


IMPORTANT DISCOVERY

Light intensity alone
does not determine whether
electrons are emitted.

The light must have
sufficient photon energy.


Since:

E = hf

the frequency must be high enough.


THRESHOLD FREQUENCY

Below a certain minimum frequency:

Electrons are not emitted,
even if the light is intense.


Above the threshold:

Photons can transfer enough energy
to release electrons.


ENERGY IDEA

Photon Energy
→ Used to free electron
→ Remaining energy may become electron kinetic energy


WHY THIS MATTERED

The photoelectric effect provided
strong evidence that light energy
behaves in discrete packets.


REAL-WORLD CONNECTION

Photoelectric principles are related to:

• Light sensors
• Photodetectors
• Solar technology
• Imaging systems


ONE-LINE TAKEAWAY

A photon must carry enough energy
to release an electron from a material.
""",

            "media_url":
                "/uploads/notes/physics/topic_10/photoelectric_effect.svg",

            "media_type":
                "svg",

            "caption":
                "A sufficiently energetic photon can transfer energy to an electron and release it from a material.",

            "alt_text":
                "Animated photon striking a metal surface and ejecting an electron."
        },


        # -------------------------------------------------
        # CHECK 2
        # -------------------------------------------------

        {
            "order": 45,

            "type": "checkpoint",

            "heading":
                "Quick Check 2 — Photon Energy",

            "body":
                "Use E = hf conceptually.",

            "interactive": {

                "question":
                    "If the frequency of light increases, what happens to the energy of each photon?",

                "options": [
                    "It increases",
                    "It decreases",
                    "It always becomes zero",
                    "It is unrelated to frequency"
                ],

                "answer":
                    "It increases",

                "explanation":
                    "Photon energy is E = hf. Since Planck's constant h is fixed, increasing frequency increases photon energy."
            }
        },


        # -------------------------------------------------
        # RADIOACTIVITY
        # -------------------------------------------------

        {
            "order": 50,

            "type": "real_world",

            "heading":
                "Radioactivity — Unstable Nuclei Can Change",

            "body": """
Not every atomic nucleus is stable.

Some nuclei spontaneously change
into more stable configurations.

During this process,
radiation can be emitted.


This phenomenon is called:

RADIOACTIVITY.


COMMON TYPES OF NUCLEAR RADIATION


ALPHA

Contains:

2 protons
+
2 neutrons


Relatively heavy.

Low penetrating power.


BETA

Often involves
high-speed electrons or positrons.

Moderate penetrating ability.


GAMMA

High-energy electromagnetic radiation.

No electric charge.

High penetrating ability.


IMPORTANT

Radioactive decay is a nuclear process.

It involves changes inside
the atomic nucleus.


HALF-LIFE

Radioactive substances decay statistically.

The HALF-LIFE is the time required
for half the radioactive nuclei
in a sample to decay.


EXAMPLE

Suppose:

Initial sample = 1000 unstable nuclei


After one half-life:

500 remain


After two half-lives:

250 remain


After three half-lives:

125 remain


REAL-WORLD APPLICATIONS

Radioactivity is used in:

• Medical diagnosis
• Cancer treatment
• Scientific research
• Industrial inspection
• Dating ancient materials
• Nuclear power


ONE-LINE TAKEAWAY

Radioactivity occurs when unstable nuclei transform
and emit radiation.
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
                "Quick Check 3 — Half-Life",

            "body":
                "Follow the repeated halving.",

            "interactive": {

                "question":
                    "A radioactive sample contains 800 unstable nuclei. After one half-life, approximately how many remain undecayed?",

                "options": [
                    "400",
                    "800",
                    "200",
                    "1600"
                ],

                "answer":
                    "400",

                "explanation":
                    "After one half-life, approximately half of the original unstable nuclei remain. Half of 800 is 400."
            }
        },


        # -------------------------------------------------
        # MASS ENERGY
        # -------------------------------------------------

        {
            "order": 60,

            "type": "animation",

            "heading":
                "Mass-Energy Equivalence",

            "body": """
Einstein showed that mass and energy
are deeply related.


The famous relationship is:

E = mc²


Where:

E = Energy

m = Mass

c = Speed of light


Because c is extremely large,
even a small amount of mass
corresponds to a very large amount of energy.


IMPORTANT

This does NOT mean that ordinary objects
are constantly releasing all of their
mass as usable energy.

It tells us that mass itself
represents a form of energy.


NUCLEAR CONNECTION

In nuclear reactions,
small differences in mass
can correspond to significant energy changes.


APPLICATIONS

This relationship is important in:

• Nuclear fission
• Nuclear fusion
• Particle physics
• Astrophysics


SUN CONNECTION

Inside the Sun,
nuclear fusion converts hydrogen
into heavier nuclei.

A small difference in mass
corresponds to released energy.

That energy eventually reaches Earth
as sunlight and heat.


ONE-LINE TAKEAWAY

Mass and energy are two connected forms
of physical quantity.
""",

            "media_url":
                "/uploads/notes/physics/topic_10/mass_energy.svg",

            "media_type":
                "svg",

            "caption":
                "Einstein's mass-energy relation shows that even a small mass corresponds to a large amount of energy.",

            "alt_text":
                "Diagram connecting mass and energy using E equals mc squared."
        },


        # -------------------------------------------------
        # SEMICONDUCTORS
        # -------------------------------------------------

        {
            "order": 70,

            "type": "application",

            "heading":
                "Modern Physics Inside Computers and Smartphones",

            "body": """
Modern Physics is not only theoretical.

It is inside the electronic devices
we use every day.


SEMICONDUCTORS

Materials such as silicon
have electrical properties
between conductors and insulators.

Their behaviour can be carefully controlled.


This allows engineers to create:

• Diodes
• Transistors
• Sensors
• Integrated circuits
• Computer processors


TRANSISTOR

A transistor can act as:

• Electronic switch
• Amplifier


Billions of tiny transistors
can exist inside a modern processor.


SOLAR CELL

Solar cells use semiconductor physics
to convert light energy
into electrical energy.


LED

A light-emitting diode converts
electrical energy into light.


CAMERA SENSOR

Modern image sensors use semiconductor devices
to detect incoming photons.


ROBOTICS CONNECTION

A robot may contain:

• Microprocessor
• Camera sensor
• Light sensors
• Motor drivers
• Memory
• Communication chips

All of these depend heavily
on semiconductor technology.


ONE-LINE TAKEAWAY

Quantum and semiconductor physics
form the foundation of modern electronics.
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
                "Quick Check 4 — Modern Technology",

            "body":
                "Connect Modern Physics with electronics.",

            "interactive": {

                "question":
                    "Which material is widely associated with semiconductor electronics and computer chips?",

                "options": [
                    "Silicon",
                    "Wood",
                    "Rubber",
                    "Paper"
                ],

                "answer":
                    "Silicon",

                "explanation":
                    "Silicon is one of the most important semiconductor materials used in transistors, integrated circuits and many electronic devices."
            }
        },


        # -------------------------------------------------
        # APPLICATIONS
        # -------------------------------------------------

        {
            "order": 80,

            "type": "application",

            "heading":
                "Where Is Modern Physics Used?",

            "body": """
💻 COMPUTERS

Semiconductor transistors form
modern processors and memory.


📱 SMARTPHONES

Modern Physics enables:

• Displays
• Cameras
• Sensors
• Processors
• Wireless communication


☀️ SOLAR CELLS

Photon energy is converted
into electrical energy.


💡 LED LIGHTING

Semiconductor transitions
produce light efficiently.


🏥 MEDICINE

Modern Physics contributes to:

• X-ray imaging
• Nuclear medicine
• Radiation therapy
• PET scanning
• MRI technologies


🌐 COMMUNICATION

Lasers and semiconductor devices
help power optical communication.


🛰️ GPS

High-precision satellite timing
requires corrections related to relativity.


⚛️ NUCLEAR ENERGY

Nuclear reactions can release
large amounts of energy.


🔬 SCIENTIFIC RESEARCH

Modern Physics helps scientists study:

• Atoms
• Nuclei
• Elementary particles
• Stars
• The universe


🤖 ROBOTICS

Modern robots rely on:

• Semiconductor processors
• Cameras
• Photodetectors
• Laser sensors
• Electronic control systems


Modern Physics is therefore deeply connected
to the technology around us.
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
MODERN PHYSICS

Explains atomic,
nuclear and quantum-scale behaviour.


ATOMS

Contain:

Nucleus
+
Electrons


ENERGY LEVELS

Electrons occupy
discrete allowed energy states.


PHOTONS

Packets of light energy.


PHOTON ENERGY

E = hf


PHOTOELECTRIC EFFECT

Sufficiently energetic photons
can release electrons from materials.


RADIOACTIVITY

Unstable nuclei can decay
and emit radiation.


HALF-LIFE

Time required for approximately
half the unstable nuclei to decay.


MASS-ENERGY RELATION

E = mc²


SEMICONDUCTORS

Provide the physical foundation
for modern electronics.


FINAL CONNECTION

Atomic Energy Levels
→ Quantum behaviour

Light Frequency
→ Photon Energy

Photon + Material
→ Photoelectric Effect

Unstable Nucleus
→ Radioactivity

Mass
→ Energy

Quantum Physics
→ Semiconductors

Semiconductors
→ Computers, smartphones and robotics


Modern Physics explains
the microscopic principles behind
many technologies that define
the modern world.
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
    print(" TOPIC 10 RICH NOTES CREATED SUCCESSFULLY")
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
        / "atomic_energy_levels.svg"
    )

    print(
        MEDIA_DIR
        / "photoelectric_effect.svg"
    )

    print(
        MEDIA_DIR
        / "mass_energy.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 10 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()