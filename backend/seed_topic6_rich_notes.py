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
    / "topic_6"
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SVG 1 — WAVE
# =========================================================

wave_svg = """
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
        How a Wave Travels
    </text>

    <line
        x1="80"
        y1="235"
        x2="920"
        y2="235"
        stroke="#cbd5e1"
        stroke-width="3"
    />

    <path
        d="M80 235
           Q130 115 180 235
           T280 235
           T380 235
           T480 235
           T580 235
           T680 235
           T780 235
           T880 235"
        fill="none"
        stroke="#4f46e5"
        stroke-width="8"
        stroke-linecap="round"
    >

        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0;40 0;0 0"
            dur="2s"
            repeatCount="indefinite"
        />

    </path>

    <line
        x1="130"
        y1="235"
        x2="130"
        y2="120"
        stroke="#16a34a"
        stroke-width="5"
    />

    <text
        x="145"
        y="155"
        font-family="Arial"
        font-size="20"
        fill="#15803d"
    >
        Amplitude
    </text>

    <line
        x1="180"
        y1="330"
        x2="380"
        y2="330"
        stroke="#dc2626"
        stroke-width="5"
    />

    <polygon
        points="180,330 200,318 200,342"
        fill="#dc2626"
    />

    <polygon
        points="380,330 360,318 360,342"
        fill="#dc2626"
    />

    <text
        x="225"
        y="370"
        font-family="Arial"
        font-size="20"
        fill="#dc2626"
    >
        Wavelength
    </text>

    <text
        x="500"
        y="395"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#172033"
    >
        Wave transfers energy without transporting matter overall
    </text>

</svg>
"""


# =========================================================
# SVG 2 — SOUND PARTICLES
# =========================================================

sound_svg = """
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
        Sound Travels Through Vibrating Particles
    </text>

    <rect
        x="80"
        y="140"
        width="90"
        height="150"
        rx="18"
        fill="#334155"
    />

    <circle
        cx="125"
        cy="215"
        r="26"
        fill="#f59e0b"
    >

        <animate
            attributeName="r"
            values="22;30;22"
            dur="0.8s"
            repeatCount="indefinite"
        />

    </circle>

    <text
        x="90"
        y="325"
        font-family="Arial"
        font-size="20"
        fill="#172033"
    >
        Speaker
    </text>

    <g fill="#6366f1">

        <circle cx="250" cy="215" r="10">
            <animate attributeName="cx" values="245;260;245" dur="1s" repeatCount="indefinite"/>
        </circle>

        <circle cx="310" cy="215" r="10">
            <animate attributeName="cx" values="305;320;305" dur="1s" repeatCount="indefinite"/>
        </circle>

        <circle cx="370" cy="215" r="10">
            <animate attributeName="cx" values="365;380;365" dur="1s" repeatCount="indefinite"/>
        </circle>

        <circle cx="430" cy="215" r="10">
            <animate attributeName="cx" values="425;440;425" dur="1s" repeatCount="indefinite"/>
        </circle>

        <circle cx="490" cy="215" r="10">
            <animate attributeName="cx" values="485;500;485" dur="1s" repeatCount="indefinite"/>
        </circle>

        <circle cx="550" cy="215" r="10">
            <animate attributeName="cx" values="545;560;545" dur="1s" repeatCount="indefinite"/>
        </circle>

        <circle cx="610" cy="215" r="10">
            <animate attributeName="cx" values="605;620;605" dur="1s" repeatCount="indefinite"/>
        </circle>

        <circle cx="670" cy="215" r="10">
            <animate attributeName="cx" values="665;680;665" dur="1s" repeatCount="indefinite"/>
        </circle>

    </g>

    <text
        x="250"
        y="150"
        font-family="Arial"
        font-size="20"
        fill="#4f46e5"
    >
        Air particles vibrate back and forth
    </text>

    <text
        x="250"
        y="330"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#ea580c"
    >
        Vibration → Compression &amp; Rarefaction → Sound Wave
    </text>

</svg>
"""


# =========================================================
# SVG 3 — FREQUENCY / PITCH
# =========================================================

frequency_svg = """
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
        Frequency Controls Pitch
    </text>

    <text
        x="85"
        y="120"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#166534"
    >
        Low Frequency → Low Pitch
    </text>

    <path
        d="M80 190
           Q140 100 200 190
           T320 190
           T440 190"
        fill="none"
        stroke="#16a34a"
        stroke-width="7"
    />

    <text
        x="570"
        y="120"
        font-family="Arial"
        font-size="22"
        font-weight="700"
        fill="#b91c1c"
    >
        High Frequency → High Pitch
    </text>

    <path
        d="M550 190
           Q575 120 600 190
           T650 190
           T700 190
           T750 190
           T800 190
           T850 190
           T900 190"
        fill="none"
        stroke="#ef4444"
        stroke-width="7"
    />

    <text
        x="290"
        y="330"
        font-family="Arial"
        font-size="24"
        font-weight="700"
        fill="#172033"
    >
        Frequency = number of vibrations per second
    </text>

    <text
        x="405"
        y="380"
        font-family="Arial"
        font-size="21"
        fill="#172033"
    >
        Unit: Hertz (Hz)
    </text>

</svg>
"""


# =========================================================
# SAVE VISUALS
# =========================================================

(
    MEDIA_DIR
    / "wave_properties.svg"
).write_text(
    wave_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "sound_particles.svg"
).write_text(
    sound_svg,
    encoding="utf-8"
)

(
    MEDIA_DIR
    / "frequency_pitch.svg"
).write_text(
    frequency_svg,
    encoding="utf-8"
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    # =====================================================
    # TOPIC 6
    # =====================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == 6
        )
        .first()
    )


    if not topic:

        raise Exception(
            "Topic 6 not found."
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
                "Waves, Sound & Vibrations",

            subtitle=
                "Understand how vibrations create waves and how sound carries energy through matter.",

            introduction=
                "From a vibrating guitar string to your phone speaker, sound begins with vibration. Waves carry that energy from one place to another.",

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
            "Waves, Sound & Vibrations"
        )

        note.subtitle = (
            "Understand how vibrations create waves and how sound carries energy through matter."
        )

        note.introduction = (
            "From a vibrating guitar string to your phone speaker, sound begins with vibration. Waves carry that energy from one place to another."
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
        # STORY
        # -------------------------------------------------

        {
            "order": 10,

            "type": "story",

            "heading":
                "What Happens When a Guitar String Vibrates?",

            "body": """
Imagine plucking a guitar string.

The string moves rapidly back and forth.

This repeated motion is called VIBRATION.


The vibrating string pushes and pulls
on the air around it.

That disturbance travels outward.

Eventually it reaches your ears.

Your brain interprets the vibration as SOUND.


THE CONNECTION

Vibration
→ Disturbance
→ Wave
→ Energy travels
→ Ear detects sound


WHAT IS A WAVE?

A wave is a disturbance that transfers energy
from one place to another.

The particles of the medium may vibrate,
but they do not travel with the wave over long distances.


EXAMPLE

When you speak:

Your vocal cords vibrate.

They make nearby air particles vibrate.

Those particles affect neighbouring particles.

The sound disturbance travels through the air.


ONE-LINE TAKEAWAY

A wave transfers energy without transporting matter overall.
""",

            "media_url":
                "/uploads/notes/physics/topic_6/wave_properties.svg",

            "media_type":
                "svg",

            "caption":
                "The disturbance travels, while particles mainly vibrate around their positions.",

            "alt_text":
                "Animated wave showing amplitude and wavelength."
        },


        # -------------------------------------------------
        # WAVE PROPERTIES
        # -------------------------------------------------

        {
            "order": 20,

            "type": "definition",

            "heading":
                "Amplitude, Wavelength and Frequency",

            "body": """
To describe a wave,
we use a few important quantities.


AMPLITUDE

Amplitude is the maximum displacement
from the equilibrium position.

For sound:

Greater amplitude generally means louder sound.


WAVELENGTH

Wavelength is the distance between
two corresponding points on consecutive waves.

For example:

Crest to crest.

Symbol:

λ


FREQUENCY

Frequency is the number of complete vibrations
or cycles produced per second.

Symbol:

f


UNIT OF FREQUENCY

Hertz

Hz


EXAMPLE

50 Hz means:

50 complete vibrations every second.


TIME PERIOD

Time period is the time taken
for one complete cycle.

Symbol:

T


RELATION

f = 1 / T


ONE-LINE TAKEAWAY

Amplitude describes size,
wavelength describes spacing,
and frequency describes how quickly the wave repeats.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # CHECKPOINT 1
        # -------------------------------------------------

        {
            "order": 25,

            "type": "checkpoint",

            "heading":
                "Quick Check 1 — Frequency",

            "body":
                "Frequency tells how many cycles occur each second.",

            "interactive": {

                "question":
                    "A vibrating source completes 100 cycles in one second. What is its frequency?",

                "options": [
                    "1 Hz",
                    "10 Hz",
                    "100 Hz",
                    "1000 Hz"
                ],

                "answer":
                    "100 Hz",

                "explanation":
                    "Frequency is the number of complete cycles per second. Therefore 100 cycles in one second means 100 Hz."
            }
        },


        # -------------------------------------------------
        # WAVE SPEED
        # -------------------------------------------------

        {
            "order": 30,

            "type": "definition",

            "heading":
                "Wave Speed — How Fast Does a Wave Travel?",

            "body": """
Wave speed connects:

Frequency
and
Wavelength.


FORMULA

v = f × λ


Where:

v = Wave speed

f = Frequency

λ = Wavelength


EXAMPLE

Frequency:

f = 5 Hz


Wavelength:

λ = 2 m


Wave speed:

v = 5 × 2

v = 10 m/s


IMPORTANT

Changing frequency does not automatically mean
the wave speed changes in the same medium.

Wave speed often depends strongly on
the properties of the medium.


ONE-LINE TAKEAWAY

Wave speed equals frequency multiplied by wavelength.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # SOUND
        # -------------------------------------------------

        {
            "order": 40,

            "type": "animation",

            "heading":
                "How Does Sound Travel Through Air?",

            "body": """
Sound is a MECHANICAL wave.

That means it requires a medium
such as:

• Air
• Water
• Solids


Sound cannot travel through a perfect vacuum.


HOW SOUND MOVES

A vibrating source pushes nearby particles.

The particles move back and forth.

This creates regions called:

COMPRESSION

Particles are closer together.


RAREFACTION

Particles are farther apart.


These compressions and rarefactions
travel through the medium.


IMPORTANT

The air itself does not travel
all the way from the speaker to your ear.

Instead:

Particle A vibrates
→ affects Particle B

Particle B vibrates
→ affects Particle C

and so on.


Energy travels through the medium.


ONE-LINE TAKEAWAY

Sound travels because neighbouring particles
transfer vibration energy.
""",

            "media_url":
                "/uploads/notes/physics/topic_6/sound_particles.svg",

            "media_type":
                "svg",

            "caption":
                "The speaker vibrates air particles, creating travelling compressions and rarefactions.",

            "alt_text":
                "Animated air particles vibrating due to a sound source."
        },


        # -------------------------------------------------
        # CHECKPOINT 2
        # -------------------------------------------------

        {
            "order": 45,

            "type": "checkpoint",

            "heading":
                "Quick Check 2 — Sound in Space",

            "body":
                "Remember that sound is a mechanical wave.",

            "interactive": {

                "question":
                    "Why can sound not travel through a perfect vacuum?",

                "options": [
                    "There are no particles to transfer the vibration",
                    "Gravity is absent",
                    "Light blocks the sound",
                    "Frequency becomes zero automatically"
                ],

                "answer":
                    "There are no particles to transfer the vibration",

                "explanation":
                    "Sound needs a material medium whose particles can vibrate and transfer energy. In a perfect vacuum there are no particles available to carry the sound wave."
            }
        },


        # -------------------------------------------------
        # PITCH
        # -------------------------------------------------

        {
            "order": 50,

            "type": "real_world",

            "heading":
                "Frequency and Pitch",

            "body": """
Why does one musical note sound high
and another sound low?

The answer is FREQUENCY.


LOW FREQUENCY

Fewer vibrations per second.

Usually perceived as:

LOWER PITCH.


HIGH FREQUENCY

More vibrations per second.

Usually perceived as:

HIGHER PITCH.


EXAMPLE

A low bass note:

Lower frequency.


A sharp whistle:

Higher frequency.


IMPORTANT

Pitch is mainly related to frequency.

Loudness is more closely related
to wave amplitude.


DO NOT CONFUSE

Frequency
→ Pitch


Amplitude
→ Loudness


REAL-WORLD CONNECTION

Music instruments control pitch
by changing vibration frequency.


ONE-LINE TAKEAWAY

Higher frequency generally produces higher pitch.
""",

            "media_url":
                "/uploads/notes/physics/topic_6/frequency_pitch.svg",

            "media_type":
                "svg",

            "caption":
                "More vibrations per second produce a higher frequency and generally a higher pitch.",

            "alt_text":
                "Comparison of low-frequency and high-frequency waves."
        },


        # -------------------------------------------------
        # CHECKPOINT 3
        # -------------------------------------------------

        {
            "order": 55,

            "type": "checkpoint",

            "heading":
                "Quick Check 3 — Pitch",

            "body":
                "Connect what you hear with frequency.",

            "interactive": {

                "question":
                    "Which change generally produces a higher-pitched sound?",

                "options": [
                    "Increasing frequency",
                    "Decreasing frequency",
                    "Removing the medium",
                    "Reducing the number of vibrations to zero"
                ],

                "answer":
                    "Increasing frequency",

                "explanation":
                    "Pitch is mainly determined by frequency. A higher frequency means more vibrations per second and is usually heard as a higher pitch."
            }
        },


        # -------------------------------------------------
        # LOUDNESS / AMPLITUDE
        # -------------------------------------------------

        {
            "order": 60,

            "type": "application",

            "heading":
                "Amplitude and Loudness",

            "body": """
Imagine gently striking a drum.

Now strike the same drum harder.

The second sound is louder.


WHY?

The harder strike produces
a larger vibration amplitude.


Greater vibration amplitude
creates a sound wave with greater amplitude.


This usually corresponds to
greater sound intensity and louder perception.


IMPORTANT

Loudness is not the same as pitch.


LOUDNESS

Closely connected with amplitude.


PITCH

Closely connected with frequency.


EXAMPLE

You can have:

A loud low-pitched sound

or

A quiet high-pitched sound.


That is because amplitude and frequency
describe different properties of the wave.
""",

            "media_url": None,
            "media_type": None,
            "caption": None,
            "alt_text": None
        },


        # -------------------------------------------------
        # REFLECTION / ECHO
        # -------------------------------------------------

        {
            "order": 70,

            "type": "application",

            "heading":
                "Reflection of Sound and Echo",

            "body": """
Sound waves can reflect
when they hit a surface.


REFLECTION

The sound wave reaches a surface
and returns toward the source.


ECHO

If the reflected sound reaches your ear
after enough delay,
you hear it as a separate sound.

That separate reflected sound is called an ECHO.


REAL-WORLD EXAMPLES

• Shouting near a mountain
• Large empty halls
• Tunnels
• Sonar systems
• Ultrasonic distance measurement


SONAR

A sound pulse is sent toward an object.

The reflected sound returns.

By measuring the travel time,
distance can be estimated.


DISTANCE IDEA

Distance travelled by sound:

Speed × Time


But because the sound travels:

Source → Object → Source

the one-way distance is often:

Distance = v × t / 2


APPLICATIONS

• Depth measurement
• Submarine navigation
• Object detection
• Ultrasonic sensors
• Medical ultrasound principles
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
            "order": 75,

            "type": "checkpoint",

            "heading":
                "Quick Check 4 — Echo Distance",

            "body":
                "Remember that the sound makes a round trip.",

            "interactive": {

                "question":
                    "An echo returns after travelling from you to a wall and back. Why is the calculated total distance divided by 2 to find the wall distance?",

                "options": [
                    "Because sound travels to the wall and then back again",
                    "Because sound speed becomes half",
                    "Because frequency is divided by two",
                    "Because the wall absorbs half the sound"
                ],

                "answer":
                    "Because sound travels to the wall and then back again",

                "explanation":
                    "The measured travel time includes the journey to the wall and the return journey. Therefore the total sound path is twice the one-way distance."
            }
        },


        # -------------------------------------------------
        # APPLICATIONS
        # -------------------------------------------------

        {
            "order": 80,

            "type": "application",

            "heading":
                "Where Are Waves and Sound Used?",

            "body": """
🎵 MUSIC

Musical instruments create controlled vibrations.

Frequency controls pitch.

Amplitude affects loudness.


📱 SMARTPHONES

Microphones convert sound vibrations
into electrical signals.

Speakers convert electrical signals
back into vibrations.


🏥 ULTRASOUND

High-frequency sound waves
can create images inside the body.


🚢 SONAR

Reflected sound waves help determine:

• Distance
• Depth
• Location of underwater objects


🤖 ROBOTICS

Ultrasonic sensors can estimate distance
using reflected sound waves.


🏢 ACOUSTIC ENGINEERING

Engineers design rooms and auditoriums
to control:

• Echo
• Reflection
• Absorption
• Sound quality


🎧 NOISE CONTROL

Understanding waves helps engineers reduce
unwanted vibration and noise.


Waves and vibrations are therefore important
in communication, medicine, sensing and engineering.
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
VIBRATION

Repeated back-and-forth motion.


WAVE

A disturbance that transfers energy.


AMPLITUDE

Maximum displacement from equilibrium.


FREQUENCY

Number of cycles per second.

Unit:

Hz


TIME PERIOD

Time for one complete cycle.

f = 1 / T


WAVELENGTH

Distance between equivalent points
on consecutive waves.


WAVE SPEED

v = fλ


SOUND

A mechanical wave.

It requires a medium.


SOUND IN AIR

Travels through:

Compressions
and
Rarefactions.


PITCH

Mainly depends on frequency.


LOUDNESS

Closely related to amplitude.


ECHO

Reflected sound heard after a delay.


FINAL CONNECTION

Vibration
→ Creates disturbance

Disturbance
→ Travels as wave

Frequency
→ Controls pitch

Amplitude
→ Influences loudness

Reflection
→ Can create echo


Waves allow energy and information
to travel from one place to another.
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
    print(" TOPIC 6 RICH NOTES CREATED SUCCESSFULLY")
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
        / "wave_properties.svg"
    )

    print(
        MEDIA_DIR
        / "sound_particles.svg"
    )

    print(
        MEDIA_DIR
        / "frequency_pitch.svg"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 6 SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()