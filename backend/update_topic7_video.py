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
    # TOPIC 7
    # =========================================================

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


    # =========================================================
    # VIDEO DETAILS
    # =========================================================

    video_title = (
        "Series & Parallel Circuits - Voltage, Current, "
        "Resistance and Ohm's Law"
    )


    video_description = (
        "A guided Physics lesson covering voltage, current, "
        "resistance, Ohm's Law, and the behaviour of series "
        "and parallel electric circuits."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=wejz5s31Cts"
    )


    learning_guide = """
BEFORE YOU WATCH

You already studied:

• Electric circuits
• Electric current
• Voltage
• Resistance
• Ohm's Law
• Series circuits
• Parallel circuits
• Electrical power

through the Rich Notes.

Now use this video to understand
how these quantities behave inside real circuits.


WHAT TO LOOK FOR

1. What is electric current?

2. What is voltage?

3. What does electrical resistance do?

4. How are V, I and R related?

5. What happens to current in a series circuit?

6. What happens to voltage in a parallel circuit?

7. How do we calculate total resistance?

8. Why are homes generally wired in parallel?


ELECTRIC CURRENT

Electric current is the rate
at which electric charge flows.


FORMULA

I = Q / t


Where:

I = Current

Q = Charge

t = Time


UNIT

Ampere

A


EXAMPLE

Charge:

Q = 12 C


Time:

t = 3 s


Current:

I = Q / t

I = 12 / 3

I = 4 A


VOLTAGE

Voltage is electrical potential difference.

It represents the energy transferred
per unit charge.


FORMULA

V = W / Q


A simple way to understand voltage:

Voltage provides the electrical push
that can drive charge through a circuit.


BATTERY CONNECTION

A battery creates a potential difference
between its terminals.

When a closed conducting path exists,
this can produce current.


RESISTANCE

Resistance opposes electric current.


Symbol:

R


Unit:

Ohm

Ω


Greater resistance generally makes
it more difficult for current to flow.


OHM'S LAW

The main relationship is:


V = I × R


From this:


I = V / R


and:


R = V / I


EXAMPLE

Voltage:

V = 12 V


Resistance:

R = 4 Ω


Current:

I = V / R

I = 12 / 4

I = 3 A


IMPORTANT CONNECTION

If resistance remains constant:

Voltage increases
→ Current increases


If voltage remains constant:

Resistance increases
→ Current decreases


SERIES CIRCUITS

In a series circuit,
components are connected
along one main current path.


CURRENT IN SERIES

The same current flows through
every component in the series path.


I₁ = I₂ = I₃


RESISTANCE IN SERIES

Total resistance is:

R_total = R₁ + R₂ + R₃ + ...


EXAMPLE

R₁ = 2 Ω

R₂ = 4 Ω


R_total = 2 + 4

R_total = 6 Ω


VOLTAGE IN SERIES

The source voltage is divided
between the series components.


V_total = V₁ + V₂ + V₃ + ...


IMPORTANT

If the series path is broken,
current through that path stops.


PARALLEL CIRCUITS

A parallel circuit contains
multiple branches.


VOLTAGE IN PARALLEL

The voltage across each branch
is the same.


V₁ = V₂ = V₃


CURRENT IN PARALLEL

The total current divides
between the branches.


I_total = I₁ + I₂ + I₃ + ...


WHY THIS MATTERS

Suppose two bulbs are connected
in separate parallel branches.

If one bulb is switched off,
the other branch can still operate.


This is one major reason
electrical systems often use parallel connections.


HOUSEHOLD CONNECTION

Household appliances are generally
connected in parallel.

This allows:

• Independent operation
• Each appliance to receive supply voltage
• One appliance to switch off
  without shutting down all other appliances


SERIES VS PARALLEL

SERIES

• One main path
• Same current
• Voltage is divided
• Resistances add


PARALLEL

• Multiple paths
• Same branch voltage
• Current divides
• Branches can operate independently


ELECTRICAL POWER

Electrical power describes
how quickly electrical energy is transferred.


FORMULA

P = V × I


Where:

P = Power

V = Voltage

I = Current


UNIT

Watt

W


EXAMPLE

Voltage:

12 V


Current:

2 A


Power:

P = VI

P = 12 × 2

P = 24 W


USING OHM'S LAW

We can also write:

P = I²R


and:

P = V² / R


ELECTRICAL ENERGY

Electrical energy transferred
over a time interval can be written as:

E = P × t


REAL-WORLD CONNECTION

A battery-powered robot contains:

Battery
→ Provides electrical energy


Power distribution
→ Sends voltage to different systems


Motor driver
→ Controls motor current


Motors
→ Convert electrical energy into motion


Sensors
→ Use electrical circuits to measure the environment


Controller
→ Processes electrical signals


So the same circuit concepts
are directly used in robotics.


SELF CHECK 1

12 C of charge passes
in 3 seconds.


I = Q / t

I = 12 / 3

I = 4 A


SELF CHECK 2

Voltage:

12 V


Resistance:

4 Ω


I = V / R

I = 3 A


SELF CHECK 3

Two resistors are connected in series:

R₁ = 3 Ω

R₂ = 5 Ω


Total resistance:

R_total = 3 + 5

R_total = 8 Ω


SELF CHECK 4

Device voltage:

10 V


Current:

3 A


Power:

P = VI

P = 10 × 3

P = 30 W


AFTER WATCHING

You should clearly understand:


CURRENT

Rate of charge flow.


VOLTAGE

Electrical potential difference.


RESISTANCE

Opposition to current.


OHM'S LAW

V = IR


SERIES CIRCUIT

One main current path.


PARALLEL CIRCUIT

Multiple current paths.


POWER

P = VI


FINAL CONNECTION

Battery
→ Creates potential difference


Voltage
→ Can drive charge


Charge flow
→ Current


Resistance
→ Opposes current


Voltage + Current + Resistance
→ Ohm's Law


Circuit arrangement
→ Determines how current and voltage are distributed


Voltage × Current
→ Electrical Power


KEY TAKEAWAY

Voltage drives electrical behaviour.

Current represents charge flow.

Resistance controls that flow.

Series and parallel connections determine
how voltage and current are distributed
through an electrical system.
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
    print(" TOPIC 7 YOUTUBE VIDEO UPDATED")
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
    print("TOPIC 7 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()