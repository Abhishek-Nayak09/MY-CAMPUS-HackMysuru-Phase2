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
    / "topic_9"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — REFLECTION
# =========================================================

reflection_svg = """
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
        Reflection of Light
    </text>

    <!-- MIRROR -->

    <line
        x1="500"
        y1="115"
        x2="500"
        y2="390"
        stroke="#475569"
        stroke-width="12"
    />

    <text
        x="520"
        y="140"
        font-family="Arial"
        font-size="20"
        fill="#475569"
    >
        Mirror
    </text>

    <!-- NORMAL -->

    <line
        x1="290"
        y1="250"
        x2="710"
        y2="250"
        stroke="#94a3b8"
        stroke-width="4"
        stroke-dasharray="12 10"
    />

    <text
        x="685"
        y="230"
        font-family="Arial"
        font-size="18"
        fill="#64748b"
    >
        Normal
    </text>

    <!-- INCIDENT RAY -->

    <line
        x1="160"
        y1="110"
        x2="490"
        y2="245"
        stroke="#ef4444"
        stroke-width="8"
    />

    <polygon
        points="500,250 474,224 472,255"
        fill="#ef4444"
    />

    <text
        x="190"
        y="125"
        font-family="Arial"
        font-size="20"
        fill="#b91c1c"
    >
        Incident Ray
    </text>

    <!-- REFLECTED RAY -->

    <line
        x1="505"
        y1="245"
        x2="835"
        y2="110"
        stroke="#2563eb"
        stroke-width="8"
    />

    <polygon
        points="850,103 817,100 829,128"
        fill="#2563eb"
    />

    <text
        x="680"
        y="125"
        font-family="Arial"
        font-size="20"
        fill="#1d4ed8"
    >
        Reflected Ray
    </text>

    <text
        x="280"
        y="420"
        font-family="Arial"
        font-size="24"
        font-weight="700"
        fill="#4338ca"
    >
        Angle of Incidence = Angle of Reflection
    </text>

</svg>
"""


# =========================================================
# SVG 2 — REFRACTION
# =========================================================

refraction_svg = """
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
        Refraction — Light Changes Direction
    </text>

    <!-- INTERFACE -->

    <line
        x1="80"
        y1="250"
        x2="920"
        y2="250"
        stroke="#0f766e"
        stroke-width="7"
    />

    <text
        x="100"
        y="225"
        font-family="Arial"
        font-size="21"
        fill="#0f766e"
    >
        Air
    </text>

    <text
        x="100"
        y="290"
        font-family="Arial"
        font-size="21"
        fill="#0369a1"
    >
        Glass / Water
    </text>

    <!-- NORMAL -->

    <line
        x1="500"
        y1="90"
        x2="500"
        y2="410"
        stroke="#94a3b8"
        stroke-width="4"
        stroke-dasharray="12 10"
    />

    <!-- INCIDENT -->

    <line
        x1="220"
        y1="110"
        x2="490"
        y2="245"
        stroke="#ef4444"
        stroke-width="8"
    />

    <polygon
        points="500,250 474,225 472,257"
        fill="#ef4444"
    />

    <!-- REFRACTED -->

    <line
        x1="505"
        y1="255"
        x2="620"
        y2="405"
        stroke="#2563eb"
        stroke-width="8"
    />

    <polygon
        points="630,420 603,397 627,390"
        fill="#2563eb"
    />

    <text
        x="220"
        y="145"
        font-family="Arial"
        font-size="20"
        fill="#b91c1c"
    >
        Incident Light
    </text>

    <text
        x="630"
        y="360"
        font-family="Arial"
        font-size="20"
        fill="#1d4ed8"
    >
        Refracted Light
    </text>

    <text
        x="235"
        y="445"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#15803d"
    >
        Light changes speed and direction when entering another medium
    </text>

</svg>
"""


# =========================================================
# SVG 3 — CONVEX LENS
# =========================================================

lens_svg = """
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
        Convex Lens — Converging Light
    </text>

    <!-- PRINCIPAL AXIS -->

    <line
        x1="70"
        y1="250"
        x2="930"
        y2="250"
        stroke="#94a3b8"
        stroke-width="4"
        stroke-dasharray="12 10"
    />

    <!-- LENS -->

    <path
        d="M475 110
           Q535 250 475 390
           Q425 250 475 110"
        fill="#bfdbfe"
        stroke="#2563eb"
        stroke-width="6"
        opacity="0.85"
    />

    <!-- INCIDENT RAYS -->

    <line
        x1="90"
        y1="150"
        x2="465"
        y2="150"
        stroke="#ef4444"
        stroke-width="7"
    />

    <line
        x1="90"
        y1="250"
        x2="465"
        y2="250"
        stroke="#ef4444"
        stroke-width="7"
    />

    <line
        x1="90"
        y1="350"
        x2="465"
        y2="350"
        stroke="#ef4444"
        stroke-width="7"
    />

    <!-- REFRACTED RAYS -->

    <line
        x1="485"
        y1="150"
        x2="760"
        y2="250"
        stroke="#16a34a"
        stroke-width="7"
    />

    <line
        x1="485"
        y1="250"
        x2="760"
        y2="250"
        stroke="#16a34a"
        stroke-width="7"
    />

    <line
        x1="485"
        y1="350"
        x2="760"
        y2="250"
        stroke="#16a34a"
        stroke-width="7"
    />

    <!-- FOCUS -->

    <circle
        cx="760"
        cy="250"
        r="13"
        fill="#7c3aed"
    >
        <animate
            attributeName="r"
            values="10;18;10"
            dur="1.2s"
            repeatCount="indefinite"
        />
    </circle>

    <text
        x="740"
        y="295"
        font-family="Arial"
        font-size="21"
        font-weight="700"
        fill="#7c3aed"
    >
        Focus
    </text>

    <text
        x="245"
        y="430"
        font-family="Arial"
        font-size="23"
        font-weight="700"
        fill="#ea580c"
    >
        Parallel rays converge near the focal point
    </text>

</svg>
"""


# =========================================================
# SAVE VISUALS
# =========================================================

(
    MEDIA_DIR
    / "reflection.svg"
).write_text(
    reflection_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "refraction.svg"
).write_text(
    refraction_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "convex_lens.svg"
).write_text(
    lens_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # TOPIC 9
    # =====================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == 9
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 9 not found."
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
                "Light & Optics",

            subtitle=
                "Understand how light travels, reflects, refracts and forms images.",

            introduction=
                "Mirrors, cameras, spectacles, telescopes and optical sensors all depend on the behaviour of light. Optics explains how light travels and how we control it using mirrors, lenses and other materials.",

            pdf_url=None,

            version=1,

            is_active=True
        )


        db.add(note)

        db.commit()

        db.refresh(note)


    else:

        note.title = (
            "Light & Optics"
        )

        note.subtitle = (
            "Understand how light travels, reflects, refracts and forms images."
        )

        note.introduction = (
            "Mirrors, cameras, spectacles, telescopes and optical sensors all depend on the behaviour of light. Optics explains how light travels and how we control it using mirrors, lenses and other materials."
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
        # LIGHT INTRO
        # -------------------------------------------------

        {
            "order": 10,

            "type": "story",

            "heading":
                "How Do We See an Object?",

            "body": """
Imagine a book lying on a table.

You can see it when light from a source
reaches the book and then reaches your eyes.


THE BASIC PATH

Light Source
→ Object
→ Eyes


If the object does not produce its own light,
we usually see it because light is reflected
from its surface.


WHAT IS LIGHT?

Light is electromagnetic radiation.

The part detectable by the human eye
is called visible light.


HOW DOES LIGHT TRAVEL?

In a uniform medium,
light travels approximately
in straight lines.


This explains:

• Shadows
• Pinhole cameras
• Ray diagrams
• Many optical systems


SPEED OF LIGHT

In vacuum,
light travels at approximately:

3 × 10^8 m/s


That is about:

300,000 km every second.


ONE-LINE TAKEAWAY

We see most objects because light reflects
from them and enters our eyes.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # REFLECTION
        # -------------------------------------------------

        {
            "order": 20,

            "type": "animation",

            "heading":
                "Reflection — Light Bouncing From a Surface",

            "body": """
When light strikes a surface
and returns into the same medium,
the process is called REFLECTION.


IMPORTANT TERMS


INCIDENT RAY

The incoming light ray.


REFLECTED RAY

The ray leaving the surface after reflection.


NORMAL

An imaginary line drawn perpendicular
to the surface at the point of incidence.


ANGLE OF INCIDENCE

The angle between:

Incident ray
and
Normal


ANGLE OF REFLECTION

The angle between:

Reflected ray
and
Normal


LAW OF REFLECTION

Angle of Incidence
=
Angle of Reflection


i = r


IMPORTANT

Angles are measured from the NORMAL,
not from the mirror surface.


REAL-WORLD EXAMPLES

• Bathroom mirror
• Rear-view mirrors
• Periscopes
• Reflecting telescopes
• Optical instruments


ONE-LINE TAKEAWAY

A reflected ray leaves at the same angle
at which the incident ray arrives,
measured relative to the normal.
""",

            "media_url":
                "/uploads/notes/physics/topic_9/reflection.svg",

            "media_type":
                "svg",

            "caption":
                "The angle of incidence equals the angle of reflection.",

            "alt_text":
                "Incident and reflected light rays at a mirror with a normal line."
        },


        # -------------------------------------------------
        # CHECK 1
        # -------------------------------------------------

        {
            "order": 25,

            "type": "checkpoint",

            "heading":
                "Quick Check 1 — Reflection",

            "body":
                "Apply the law of reflection.",

            "interactive": {

                "question":
                    "A light ray strikes a mirror at an angle of 30° to the normal. What is the angle of reflection?",

                "options": [
                    "30°",
                    "60°",
                    "90°",
                    "15°"
                ],

                "answer":
                    "30°",

                "explanation":
                    "According to the law of reflection, the angle of incidence equals the angle of reflection. Therefore the reflected angle is 30°."
            }
        },


        # -------------------------------------------------
        # REFRACTION
        # -------------------------------------------------

        {
            "order": 30,

            "type": "real_world",

            "heading":
                "Refraction — Why Does a Straw Look Bent in Water?",

            "body": """
Place a straw inside a glass of water.

The straw may appear bent
at the water surface.

The straw itself is not actually bent.

The effect occurs because light changes direction
when it passes between different media.

This is called REFRACTION.


WHY DOES REFRACTION OCCUR?

Light travels at different speeds
in different materials.


When light enters another medium
at an angle,
its speed changes.

Its direction can therefore change.


EXAMPLES

Air → Water

Air → Glass

Glass → Air


OPTICAL DENSITY

Materials affect the speed of light differently.

When light enters a medium
where it travels more slowly,
the ray generally bends toward the normal.

When it enters a medium
where it travels faster,
it generally bends away from the normal.


REAL-WORLD EXAMPLES

• Straw appearing bent in water
• Swimming pool appearing shallower
• Spectacles
• Cameras
• Microscopes
• Telescopes


ONE-LINE TAKEAWAY

Refraction occurs because light changes speed
when moving between different media.
""",

            "media_url":
                "/uploads/notes/physics/topic_9/refraction.svg",

            "media_type":
                "svg",

            "caption":
                "Light can change direction when its speed changes at the boundary between two media.",

            "alt_text":
                "Light ray bending when passing from air into another transparent medium."
        },


        # -------------------------------------------------
        # REFRACTIVE INDEX
        # -------------------------------------------------

        {
            "order": 40,

            "type": "definition",

            "heading":
                "Refractive Index",

            "body": """
The refractive index tells us
how much light slows down
inside a material compared with vacuum.


FORMULA

n = c / v


Where:

n = Refractive Index

c = Speed of light in vacuum

v = Speed of light in the material


EXAMPLE

Suppose light travels through a material at:

2 × 10^8 m/s


Speed in vacuum:

3 × 10^8 m/s


Then:

n = c / v

n = 3 × 10^8 / 2 × 10^8

n = 1.5


INTERPRETATION

A refractive index of 1.5 means
light travels more slowly in that medium
than in vacuum.


SNELL'S LAW

Refraction between two media can be described by:

n₁ sin θ₁
=
n₂ sin θ₂


This connects:

• Refractive indices
• Incident angle
• Refracted angle


ONE-LINE TAKEAWAY

Refractive index measures
how strongly a material affects light speed.
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
            "order": 45,

            "type": "checkpoint",

            "heading":
                "Quick Check 2 — Refractive Index",

            "body":
                "Use n = c / v.",

            "interactive": {

                "question":
                    "Light travels at 2 × 10^8 m/s in a material. If its vacuum speed is 3 × 10^8 m/s, what is the refractive index?",

                "options": [
                    "1.5",
                    "0.67",
                    "6",
                    "5"
                ],

                "answer":
                    "1.5",

                "explanation":
                    "n = c / v = (3 × 10^8) / (2 × 10^8) = 1.5."
            }
        },


        # -------------------------------------------------
        # LENSES
        # -------------------------------------------------

        {
            "order": 50,

            "type": "animation",

            "heading":
                "Lenses — Controlling the Direction of Light",

            "body": """
A lens is a transparent optical component
that changes the direction of light
through refraction.


Two important lens types are:


CONVEX LENS

Thicker near the centre.

Usually called a:

CONVERGING LENS.


Parallel light rays can converge
toward a focal point.


CONCAVE LENS

Thinner near the centre.

Usually called a:

DIVERGING LENS.


Parallel rays spread outward
after passing through it.


FOCAL POINT

The point where parallel rays converge,
or appear to diverge from,
is related to the focal point.


FOCAL LENGTH

The distance between the optical centre
of the lens and its principal focus
is called focal length.


REAL-WORLD USE

Convex lenses are used in:

• Cameras
• Magnifying glasses
• Microscopes
• Telescopes
• Human-eye correction


Concave lenses are used in:

• Certain spectacles
• Optical systems
• Beam expansion


ONE-LINE TAKEAWAY

Lenses use refraction to converge
or diverge light rays.
""",

            "media_url":
                "/uploads/notes/physics/topic_9/convex_lens.svg",

            "media_type":
                "svg",

            "caption":
                "A convex lens can make parallel rays converge near its focal point.",

            "alt_text":
                "Parallel light rays passing through a convex lens and converging at a focus."
        },


        # -------------------------------------------------
        # CHECK 3
        # -------------------------------------------------

        {
            "order": 55,

            "type": "checkpoint",

            "heading":
                "Quick Check 3 — Convex Lens",

            "body":
                "Identify how a convex lens behaves.",

            "interactive": {

                "question":
                    "What generally happens to parallel rays passing through a convex lens?",

                "options": [
                    "They converge",
                    "They stop completely",
                    "They always reflect backward",
                    "They disappear"
                ],

                "answer":
                    "They converge",

                "explanation":
                    "A convex lens is a converging lens. Parallel rays are refracted toward a focal region."
            }
        },


        # -------------------------------------------------
        # IMAGE FORMATION
        # -------------------------------------------------

        {
            "order": 60,

            "type": "definition",

            "heading":
                "Real Images and Virtual Images",

            "body": """
Optical systems can produce
different types of images.


REAL IMAGE

A real image forms where
light rays actually converge.

A real image can generally be projected
onto a screen.


EXAMPLE

A camera lens focuses light
onto the camera sensor.

That is a real image.


VIRTUAL IMAGE

A virtual image forms where
light rays only appear to originate.

The rays do not physically converge
at the image position.


A virtual image cannot normally
be projected directly onto a screen.


EXAMPLE

The image seen in a plane mirror
is virtual.


PLANE MIRROR IMAGE

A plane mirror usually creates an image that is:

• Virtual
• Upright
• Same approximate size as object
• Laterally inverted
• Appears behind the mirror


ONE-LINE TAKEAWAY

Real images involve actual ray convergence;
virtual images involve apparent ray origins.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # LIGHT SPECTRUM
        # -------------------------------------------------

        {
            "order": 70,

            "type": "application",

            "heading":
                "White Light and the Visible Spectrum",

            "body": """
White light contains
many visible wavelengths.


When white light passes through
a suitable prism,
different wavelengths refract
by different amounts.

The light can separate
into visible colours.


This process is called:

DISPERSION.


VISIBLE COLOURS

Commonly represented as:

• Violet
• Indigo
• Blue
• Green
• Yellow
• Orange
• Red


WHY DOES THIS HAPPEN?

Different wavelengths experience
slightly different refractive behaviour
inside the material.


RAINBOW CONNECTION

Water droplets can:

• Refract sunlight
• Disperse the light
• Reflect light internally
• Refract it again

producing the colours seen in a rainbow.


IMPORTANT

Visible light is only a small part
of the electromagnetic spectrum.


Other regions include:

• Radio waves
• Microwaves
• Infrared
• Ultraviolet
• X-rays
• Gamma rays
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
                "Quick Check 4 — Dispersion",

            "body":
                "Think about what a prism does to white light.",

            "interactive": {

                "question":
                    "What is the separation of white light into different visible colours called?",

                "options": [
                    "Dispersion",
                    "Conduction",
                    "Momentum",
                    "Induction"
                ],

                "answer":
                    "Dispersion",

                "explanation":
                    "Dispersion occurs because different wavelengths of visible light refract by different amounts."
            }
        },


        # -------------------------------------------------
        # APPLICATIONS
        # -------------------------------------------------

        {
            "order": 80,

            "type": "application",

            "heading":
                "Where Is Optics Used?",

            "body": """
📷 CAMERAS

Lenses focus light
onto an image sensor.


👓 EYEGLASSES

Corrective lenses modify
how incoming light is focused.


🔬 MICROSCOPES

Lens systems enlarge
very small objects.


🔭 TELESCOPES

Optical systems collect
and focus light from distant objects.


📱 SMARTPHONES

Phone cameras use:

• Multiple lenses
• Image sensors
• Autofocus systems
• Optical stabilization


🤖 ROBOTICS

Robots use cameras and optical sensors
for:

• Object detection
• Navigation
• Mapping
• Distance estimation
• Visual inspection


🏥 MEDICINE

Optical technologies are used in:

• Endoscopy
• Imaging systems
• Laser procedures
• Diagnostic instruments


🌐 FIBER OPTICS

Light carries information
through optical fibres.

This enables high-speed communication.


🚘 AUTONOMOUS SYSTEMS

Cameras and optical sensors help systems detect:

• Roads
• Objects
• Signs
• People
• Obstacles


Optics is therefore central
to communication, imaging,
automation and sensing.
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
LIGHT

Travels approximately in straight lines
through a uniform medium.


REFLECTION

Light returns from a surface.

Angle of incidence
=
Angle of reflection.


REFRACTION

Light changes speed and direction
when entering another medium.


REFRACTIVE INDEX

n = c / v


CONVEX LENS

Converges parallel light rays.


CONCAVE LENS

Diverges parallel light rays.


REAL IMAGE

Light rays actually converge.

Can generally be projected.


VIRTUAL IMAGE

Light rays only appear
to originate from the image location.


DISPERSION

White light separates
into component colours.


FINAL CONNECTION

Light strikes surface
→ Reflection

Light enters new medium
→ Refraction

Refraction through lens
→ Image formation

Different wavelengths refract differently
→ Dispersion

Controlled light
→ Cameras, spectacles, microscopes,
telescopes and optical sensors


Optics is the science of
how light behaves and how we control it.
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
    print(" TOPIC 9 RICH NOTES CREATED SUCCESSFULLY")
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
        / "reflection.svg"
    )

    print(
        MEDIA_DIR
        / "refraction.svg"
    )

    print(
        MEDIA_DIR
        / "convex_lens.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 9 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()