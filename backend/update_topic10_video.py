from app.db.database import SessionLocal

from app.models.user import User
from app.models.course import Course
from app.models.year import AcademicYear
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic
from app.models.learning_content import LearningContent


db = SessionLocal()


try:

    # =========================================================
    # TOPIC 10
    # =========================================================

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


    # =========================================================
    # VERIFIED ENGLISH VIDEO
    # =========================================================

    video_title = (
        "Modern Physics - Quantum, Atomic, Nuclear Physics "
        "& Photoelectric Effect"
    )


    video_description = (
        "English Modern Physics lesson covering atomic structure, "
        "quantum ideas, photoelectric effect, radioactivity, "
        "half-life, nuclear physics, fission and fusion."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=oqRzaiUcYwk"
    )


    learning_guide = """
BEFORE YOU WATCH

LANGUAGE:

ENGLISH


You have already studied:

• Atomic energy levels
• Quantized energy
• Photons
• Photoelectric effect
• Radioactivity
• Half-life
• Mass-energy equivalence
• Semiconductors

through the My Campus Rich Notes.


Use this video to connect these ideas
into one Modern Physics picture.


WHAT TO FOCUS ON

1. Why classical Physics was not enough

2. Atomic structure

3. Quantized energy

4. Photon behaviour

5. Photoelectric effect

6. Threshold frequency

7. Radioactive decay

8. Half-life

9. Nuclear physics

10. Nuclear fission and fusion


WHY MODERN PHYSICS?

Classical Physics explains many things well:

• Motion
• Forces
• Machines
• Waves
• Electricity


But when scientists studied:

• Atoms
• Electrons
• Light
• Nuclear processes

new physical ideas were required.


This led to:

MODERN PHYSICS


ATOMIC STRUCTURE

An atom contains a small central:

NUCLEUS


The nucleus contains:

• Protons
• Neutrons


Electrons exist around the nucleus.


QUANTIZED ENERGY

In modern atomic Physics,
electrons cannot simply possess
any arbitrary atomic energy.


They occupy allowed:

ENERGY LEVELS


This means atomic energy
is QUANTIZED.


QUANTIZED means:

Only particular discrete
energy values are allowed.


ENERGY TRANSITION

An electron can absorb energy
and move to a higher energy state.


Lower Energy Level

↓

Absorb Energy

↓

Higher Energy Level


An electron can also return
to a lower energy level.


Higher Energy Level

↓

Lower Energy Level

↓

Energy Released


That released energy can appear
as electromagnetic radiation.


PHOTONS

Modern Physics describes light energy
as being carried in packets called:

PHOTONS


PHOTON ENERGY

E = h × f


Where:

E = Photon energy

h = Planck's constant

f = Frequency


IMPORTANT CONNECTION

Higher Frequency

→ Higher Photon Energy


Lower Frequency

→ Lower Photon Energy


CONNECT WITH WAVES

Earlier you learned:

Frequency describes
cycles per second.


Modern Physics adds:

For electromagnetic radiation,
frequency determines
the energy of each photon.


PHOTOELECTRIC EFFECT

When sufficiently energetic light
falls on certain materials,
electrons can be emitted.


This is called:

PHOTOELECTRIC EFFECT


PHOTON

↓

Transfers Energy

↓

Electron

↓

Electron may escape material


THRESHOLD FREQUENCY

There is a minimum frequency
required before photoelectric emission
can occur for a given material.


Below threshold frequency:

Electrons are not emitted
by simply increasing brightness.


Why?


Because each photon still
does not contain enough energy.


Remember:

E = hf


Higher frequency means
greater energy per photon.


WHY PHOTOELECTRIC EFFECT IS IMPORTANT

It provided important evidence
for the particle-like behaviour of light
and the quantum nature of energy.


REAL-WORLD CONNECTIONS

Related photoelectric and photon principles
are important in:

• Photodetectors
• Light sensors
• Imaging devices
• Solar technology


RADIOACTIVITY

Some atomic nuclei are unstable.


An unstable nucleus may spontaneously
transform into another state
while emitting radiation.


This is called:

RADIOACTIVITY


COMMON RADIATION TYPES

ALPHA

Contains:

2 protons
+
2 neutrons


BETA

Can involve energetic
electrons or positrons.


GAMMA

High-energy electromagnetic radiation.


HALF-LIFE

Radioactive decay is statistical.


HALF-LIFE means:

The time required for approximately
half of the unstable nuclei
in a sample to decay.


EXAMPLE

Initial nuclei:

800


After one half-life:

400


After two half-lives:

200


After three half-lives:

100


IMPORTANT

Half-life does NOT mean
all atoms disappear
after two half-lives.


The amount keeps reducing
by approximately half.


NUCLEAR PHYSICS

Nuclear Physics studies:

• Atomic nuclei
• Nuclear forces
• Radioactive decay
• Nuclear reactions


Two important nuclear processes are:

FISSION

and

FUSION


NUCLEAR FISSION

A heavy nucleus splits
into smaller nuclei.


This process can release energy.


Fission is important in:

• Nuclear reactors
• Nuclear-energy research


NUCLEAR FUSION

Smaller nuclei combine
to form a heavier nucleus.


Fusion can release
very large amounts of energy.


SUN CONNECTION

The Sun produces energy
primarily through nuclear fusion.


Hydrogen nuclei ultimately contribute
to forming heavier nuclei.


Energy is released in the process.


MASS-ENERGY CONNECTION

Einstein showed:

E = mc²


Where:

E = Energy

m = Mass

c = Speed of light


Because:

c²

is extremely large,

even a small mass difference
can correspond to significant energy.


This idea is important
in understanding nuclear reactions.


FISSION VS FUSION

FISSION

Heavy nucleus

→ Splits

→ Smaller nuclei + Energy


FUSION

Light nuclei

→ Combine

→ Heavier nucleus + Energy


SEMICONDUCTOR CONNECTION

Our Rich Notes also connect
Modern Physics with electronics.


Semiconductors such as silicon
allow us to build:

• Diodes
• Transistors
• Sensors
• Integrated circuits
• Processors


TRANSISTORS

Transistors can act as:

• Electronic switches
• Amplifiers


Billions of transistors
can exist inside modern processors.


MODERN PHYSICS IN YOUR PHONE

Your smartphone uses Modern Physics
everywhere.


PROCESSOR

→ Semiconductor Physics


CAMERA SENSOR

→ Photon detection


DISPLAY

→ Semiconductor / optical Physics


MEMORY

→ Electronic devices


COMMUNICATION

→ Electromagnetic radiation


GPS

→ Precise timing and relativity corrections


SELF CHECK 1

What does quantized energy mean?

Answer:

Only particular discrete energy values
are allowed.


SELF CHECK 2

What happens to photon energy
when frequency increases?

Answer:

Photon energy increases.


Because:

E = hf


SELF CHECK 3

A radioactive sample begins
with 800 unstable nuclei.

After one half-life:

400 remain.


SELF CHECK 4

Which nuclear process powers the Sun?

Answer:

Nuclear fusion.


REAL-WORLD APPLICATIONS

Modern Physics supports:

• Computers
• Smartphones
• Solar cells
• LEDs
• Lasers
• Cameras
• Medical imaging
• Radiation therapy
• Nuclear energy
• Satellites
• GPS
• Scientific instruments


ROBOTICS CONNECTION

A modern robot contains technology
built on Modern Physics.


PROCESSOR

Semiconductor Physics


CAMERA

Photon detection


LiDAR

Laser light


SENSORS

Semiconductor devices


COMMUNICATION

Electromagnetic waves


Modern Physics therefore sits
under many technologies used
inside intelligent machines.


AFTER WATCHING

You should understand:


QUANTIZATION

Only particular energy states
are allowed.


PHOTON

Packet of electromagnetic energy.


PHOTON ENERGY

E = hf


PHOTOELECTRIC EFFECT

Sufficiently energetic photons
can release electrons.


RADIOACTIVITY

Unstable nuclei can spontaneously decay.


HALF-LIFE

Time for approximately half
the radioactive nuclei to decay.


FISSION

Heavy nucleus splits.


FUSION

Light nuclei combine.


MASS-ENERGY RELATION

E = mc²


SEMICONDUCTORS

Foundation of modern electronics.


FINAL CONNECTION

Atom

→ Energy Levels


Energy Levels

→ Quantum Physics


Light

→ Photons


Photon Frequency

→ Photon Energy


Photon + Material

→ Photoelectric Effect


Unstable Nucleus

→ Radioactivity


Nuclear Reactions

→ Energy


Quantum Physics

→ Semiconductor Technology


Semiconductors

→ Modern Computers & Robotics


KEY TAKEAWAY

Modern Physics explains the behaviour
of matter and energy at scales
where classical Physics is no longer enough.

Those ideas now form the foundation
of many technologies we use every day.
"""


    # =========================================================
    # FIND EXISTING VIDEO
    # =========================================================

    video = (
        db.query(LearningContent)
        .filter(
            LearningContent.topic_id == topic.id,
            LearningContent.resource_type == "video"
        )
        .first()
    )


    # =========================================================
    # CREATE / UPDATE
    # =========================================================

    if not video:

        video = LearningContent(

            topic_id=
                topic.id,

            resource_type=
                "video",

            title=
                video_title,

            description=
                video_description,

            content_text=
                learning_guide,

            resource_url=
                youtube_url,

            content_order=
                2,

            uploaded_by=
                None,

            is_active=
                True
        )

        db.add(video)


    else:

        video.title = video_title

        video.description = video_description

        video.content_text = learning_guide

        video.resource_url = youtube_url

        video.content_order = 2

        video.is_active = True


    # =========================================================
    # SAVE
    # =========================================================

    db.commit()

    db.refresh(video)


    # =========================================================
    # VERIFY
    # =========================================================

    print("")
    print("==========================================")
    print(" TOPIC 10 ENGLISH VIDEO UPDATED")
    print("==========================================")
    print("")

    print(
        f"Topic ID : {topic.id}"
    )

    print(
        f"Topic    : {topic.title}"
    )

    print(
        f"Video ID : {video.id}"
    )

    print(
        f"Title    : {video.title}"
    )

    print(
        f"URL      : {video.resource_url}"
    )

    print(
        f"Active   : {video.is_active}"
    )

    print(
        "Language : English"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 10 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()