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
    # TOPIC 8
    # =========================================================

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


    # =========================================================
    # VIDEO DETAILS
    # =========================================================

    video_title = (
        "Magnetic Effects of Electric Current"
    )


    video_description = (
        "A guided Physics lesson covering magnetic fields, "
        "magnetic effects of electric current, solenoids, "
        "electromagnets and electromagnetic induction."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=Tk1RGdqxVXQ"
    )


    learning_guide = """
BEFORE YOU WATCH

You already studied:

• Magnetic poles
• Magnetic fields
• Earth's magnetic field
• Magnetic effect of electric current
• Electromagnets
• Electric motors
• Electromagnetic induction
• Generators

through the Rich Notes.

Now use this video to connect
electricity and magnetism as one system.


WHAT TO LOOK FOR

1. What is a magnetic field?

2. How do magnetic poles interact?

3. How can electric current create magnetism?

4. What happens around a current-carrying wire?

5. What is a solenoid?

6. How does an electromagnet work?

7. How can magnetic fields produce mechanical motion?

8. How can changing magnetic fields produce electricity?


MAGNETIC POLES

A magnet has two poles:

North Pole

and

South Pole.


IMPORTANT RULE

Unlike poles attract.

North + South
→ Attraction


Like poles repel.

North + North
→ Repulsion

South + South
→ Repulsion


MAGNETIC FIELD

A magnetic field is a region
where magnetic forces can act.


Magnetic field lines are used
to represent:

• Direction
• Shape
• Relative strength of the field


For a bar magnet,
outside the magnet:

Field direction is conventionally:

North
→ South


The field is generally stronger
where field lines are more closely packed.


EARTH'S MAGNETIC FIELD

Earth behaves approximately
like a large magnetic system.

A compass needle aligns
with Earth's magnetic field.


This principle helps explain
magnetic navigation.


ELECTRIC CURRENT CREATES MAGNETISM

One of the most important ideas
in electromagnetism is:

Electric current produces
a magnetic field.


Imagine a straight wire.

When no current flows:

There is no current-produced magnetic field.


When current flows:

A magnetic field forms
around the conductor.


The field lines around
a straight current-carrying wire
form approximately concentric circles.


RIGHT-HAND THUMB RULE

Point your right thumb
in the direction of conventional current.

Your curled fingers indicate
the direction of the magnetic field
around the conductor.


IMPORTANT CONNECTION

Current Direction Changes
→ Magnetic Field Direction Changes


CURRENT THROUGH A COIL

Now imagine bending the wire
into a circular loop.

Each part of the loop
creates a magnetic field.


These magnetic effects combine.


If many loops are placed together,
we form a coil called a:

SOLENOID


SOLENOID

A current-carrying solenoid
produces a magnetic field similar
to that of a bar magnet.


It has:

One magnetic north side

and

One magnetic south side.


ELECTROMAGNET

Place a suitable iron core
inside a current-carrying coil.

The magnetic effect becomes stronger.


This forms an:

ELECTROMAGNET


WHY ELECTROMAGNETS ARE USEFUL

Unlike a permanent magnet,
an electromagnet can be controlled.


CURRENT ON

→ Magnetic field produced


CURRENT OFF

→ Magnetic effect greatly reduced


HOW TO STRENGTHEN AN ELECTROMAGNET

Generally:

Increase current
→ Stronger field


Increase coil turns
→ Stronger field


Use suitable iron core
→ Stronger electromagnet


REAL-WORLD APPLICATIONS

Electromagnets are used in:

• Relays
• Electric bells
• Magnetic locks
• Solenoids
• Industrial lifting magnets
• Speakers
• Electric motors


FORCE ON A CURRENT-CARRYING CONDUCTOR

A current-carrying conductor
placed inside an external magnetic field
can experience a force.


This is extremely important because
it allows electrical energy
to create mechanical motion.


This principle is used
inside electric motors.


ELECTRIC MOTOR

An electric motor converts:

Electrical Energy

into:

Mechanical Energy


BASIC IDEA

Current flows through a conductor or coil.

The conductor is placed
inside a magnetic field.

Magnetic forces act
on the current-carrying conductor.

These forces can produce:

ROTATION


ROBOTICS CONNECTION

Robot drive motor:

Battery
→ Electrical energy

Motor driver
→ Controls current

Motor coils
→ Produce electromagnetic interaction

Magnetic force
→ Produces torque

Motor shaft
→ Rotates

Wheel
→ Robot moves


This is the direct connection
between electromagnetism and robotics.


MOTOR ENERGY CONVERSION

Electrical Energy
→ Magnetic Interaction
→ Mechanical Rotation


ELECTROMAGNETIC INDUCTION

Electric current can create magnetism.

But the relationship can also
work in the opposite direction.


A changing magnetic field
can induce an electrical voltage.


This is called:

ELECTROMAGNETIC INDUCTION


SIMPLE EXAMPLE

Take:

A coil of wire

and

A magnet.


Move the magnet toward the coil.

The magnetic environment
through the coil changes.

A voltage can be induced.


Stop changing the magnetic field.

The induced effect changes.


KEY IDEA

It is the CHANGE in magnetic conditions
that is important.


GENERATOR

A generator uses
electromagnetic induction.


GENERATOR ENERGY CONVERSION

Mechanical Energy

→

Electrical Energy


HOW?

Mechanical motion changes
the magnetic field relationship
between conductors and magnets.

This induces electrical voltage.


MOTOR VS GENERATOR

MOTOR

Electrical Energy
→ Mechanical Energy


GENERATOR

Mechanical Energy
→ Electrical Energy


They demonstrate two sides
of electromagnetism.


REAL-WORLD GENERATORS

Generators are used in:

• Hydroelectric plants
• Wind turbines
• Thermal power plants
• Alternators
• Bicycle dynamos
• Backup generators


SPEAKER CONNECTION

A speaker contains a coil
inside a magnetic field.

Electrical audio signals
change current through the coil.

Magnetic forces move the coil
and speaker cone.

The cone vibrates.

Those vibrations create sound waves.


CONNECT WITH TOPIC 6

Electrical Signal
→ Electromagnetic Force
→ Vibration
→ Sound Wave


This connects:

Electricity

Magnetism

Mechanical vibration

Sound


SELF CHECK 1

What happens when
electric current flows through a wire?

Answer:

A magnetic field forms
around the conductor.


SELF CHECK 2

How can an electromagnet
generally be strengthened?

Examples:

• Increase current
• Increase coil turns
• Use suitable iron core


SELF CHECK 3

What does an electric motor convert?

Electrical Energy
→ Mechanical Energy


SELF CHECK 4

What does a generator convert?

Mechanical Energy
→ Electrical Energy


ROBOTICS APPLICATIONS

Electromagnetism is used in:

• DC motors
• Servo motors
• Stepper motors
• Solenoid actuators
• Relays
• Speakers
• Magnetic sensors
• Encoders
• Power systems


AFTER WATCHING

You should clearly understand:


MAGNETIC FIELD

Region where magnetic forces act.


CURRENT

Produces a magnetic field.


SOLENOID

A coil producing a magnetic field
when current flows.


ELECTROMAGNET

A controllable magnet
created using electric current.


MOTOR

Electricity
→ Motion


ELECTROMAGNETIC INDUCTION

Changing magnetic field
→ Induced voltage


GENERATOR

Motion
→ Electricity


FINAL CONNECTION

Magnet
→ Magnetic Field


Electric Current
→ Magnetic Field


Current + Coil
→ Stronger Magnetic Effect


Coil + Iron Core
→ Electromagnet


Current + External Magnetic Field
→ Force


Force
→ Motor Rotation


Changing Magnetic Field
→ Induced Voltage


Induced Voltage
→ Generator Output


KEY TAKEAWAY

Electricity can create magnetism.

Magnetism can create forces.

Changing magnetism can create electricity.

That three-way connection
is the foundation of electromagnetism.
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

        video.title = (
            video_title
        )

        video.description = (
            video_description
        )

        video.content_text = (
            learning_guide
        )

        video.resource_url = (
            youtube_url
        )

        video.content_order = (
            2
        )

        video.is_active = (
            True
        )


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
    print(" TOPIC 8 YOUTUBE VIDEO UPDATED")
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

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 8 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()