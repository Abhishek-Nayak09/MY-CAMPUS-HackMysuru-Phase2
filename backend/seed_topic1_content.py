from app.db.database import SessionLocal

# Import all dependent models so SQLAlchemy
# can resolve every foreign key correctly.
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
            "Topic not found. Run Physics seed first."
        )


    # =========================================================
    # CONTENT DATA
    # =========================================================

    contents = [

        # -----------------------------------------------------
        # NOTES
        # -----------------------------------------------------

        {
            "resource_type": "notes",

            "title":
                "Why Do We Study Physics?",

            "description":
                "A simple introduction to Physics and its importance in everyday life.",

            "content_order": 1,

            "resource_url": None,

            "content_text": """
WHAT IS PHYSICS?

Physics is the branch of science that studies matter,
energy, motion, forces, space and time.

In simple words:

Physics helps us understand HOW and WHY things happen
around us.


WHY SHOULD WE LEARN PHYSICS?

Physics explains many things we experience every day.

Examples:

1. Why does a ball fall to the ground?
   → Gravity

2. Why does a moving bicycle stop when brakes are applied?
   → Friction

3. Why does a car require more force to accelerate faster?
   → Newton's Laws of Motion

4. How does electricity light a bulb?
   → Electric current and energy

5. How can we hear music?
   → Sound waves

6. How can mirrors form images?
   → Reflection of light


PHYSICS IN REAL LIFE

SPORTS

When a football player kicks a ball, several Physics
concepts are involved:

• Force
• Motion
• Energy
• Momentum
• Gravity


VEHICLES

Cars, bikes and trains use Physics in:

• Acceleration
• Braking
• Friction
• Momentum
• Aerodynamics
• Energy conversion


BUILDINGS AND BRIDGES

Engineers use Physics to calculate:

• Forces
• Loads
• Balance
• Stress
• Stability

Without Physics, safe structures cannot be designed.


SMARTPHONES

A smartphone uses several areas of Physics:

• Electricity
• Electromagnetic waves
• Light
• Sound
• Semiconductor technology


MEDICINE

Physics is important in medical technologies such as:

• X-rays
• MRI
• Ultrasound
• Laser treatment
• Radiation therapy


SPACE TECHNOLOGY

Rockets and satellites depend on:

• Newton's Laws
• Gravity
• Momentum
• Energy
• Orbital motion


ENGINEERING AND PHYSICS

Almost every engineering field uses Physics.

Mechanical Engineering:
Motion, force, heat and energy.

Civil Engineering:
Structures, forces and materials.

Electrical Engineering:
Electricity and electromagnetism.

Electronics Engineering:
Semiconductors and waves.

Computer Engineering:
Electronics, communication and hardware.


KEY IDEA

Physics is not only a subject containing equations.

Physics is a tool used to understand,
predict and design the physical world.
"""
        },


        # -----------------------------------------------------
        # VIDEO
        # -----------------------------------------------------

        {
            "resource_type": "video",

            "title":
                "Physics Around Us — Visual Explanation",

            "description":
                "A short visual lesson explaining how Physics appears in everyday life.",

            "content_order": 2,

            "resource_url": None,

            "content_text": """
VIDEO LESSON SCRIPT

Imagine waking up in the morning.

Your alarm produces sound waves.

When you switch on the light,
electrical energy becomes light energy.

When you walk,
friction between your feet and the floor
helps you move forward.

When you travel in a car,
Newton's Laws explain acceleration and braking.

When you use your smartphone,
electromagnetic waves carry information.

When you play football,
force, velocity, gravity and momentum
determine how the ball moves.

When doctors use MRI, ultrasound or X-rays,
they are applying Physics to understand the human body.

When a rocket travels into space,
gravity, momentum and Newton's Laws
control its motion.

Physics is therefore not limited to a classroom.

It is present in transportation,
sports, medicine, communication,
construction, energy and space technology.

Understanding Physics helps us understand
the world and create new technology.
"""
        },


        # -----------------------------------------------------
        # VISUALIZATION
        # -----------------------------------------------------

        {
            "resource_type": "visualization",

            "title":
                "Interactive World of Physics",

            "description":
                "Explore real-world objects and discover the Physics concepts working inside them.",

            "content_order": 3,

            "resource_url": None,

            "content_text": """
INTERACTIVE VISUALIZATION

1. FOOTBALL

Force → starts motion
Velocity → speed and direction
Gravity → pulls downward
Momentum → depends on mass and velocity


2. CAR

Engine force → moves vehicle
Friction → tyre grip
Brakes → reduce motion
Momentum → affects stopping distance


3. BRIDGE

Weight → acts downward
Support forces → act upward
Balanced forces → keep the bridge stable


4. SMARTPHONE

Electricity → powers circuits
Electromagnetic waves → communication
Light → screen
Sound waves → speaker and microphone


5. HOSPITAL

X-rays → imaging
Ultrasound → sound-wave imaging
MRI → magnetic fields and radio waves


6. ROCKET

Action → gases pushed downward
Reaction → rocket moves upward
Gravity → pulls toward Earth
Momentum → changes during propulsion
"""
        },


        # -----------------------------------------------------
        # GAME
        # -----------------------------------------------------

        {
            "resource_type": "game",

            "title":
                "Find the Physics Around You",

            "description":
                "Match real-world situations with the correct Physics concept.",

            "content_order": 4,

            "resource_url": None,

            "content_text": """
GAME: FIND THE PHYSICS AROUND YOU

QUESTION 1

A football falls back to the ground
after being kicked upward.

Correct Answer:
Gravity


QUESTION 2

A car slows down when the driver
presses the brake.

Correct Answer:
Friction and Force


QUESTION 3

A mobile phone communicates
without wires.

Correct Answer:
Electromagnetic Waves


QUESTION 4

Doctors use ultrasound to observe
internal organs.

Correct Answer:
Sound Waves


QUESTION 5

A rocket pushes gases downward
and moves upward.

Correct Answer:
Newton's Third Law


QUESTION 6

A bridge remains stationary
while carrying vehicles.

Correct Answer:
Balanced Forces


SCORING

6/6 → Physics Explorer

4–5 → Good Understanding

0–3 → Review the visualization again
"""
        }

    ]


    # =========================================================
    # INSERT / UPDATE
    # =========================================================

    for item in contents:

        existing = (
            db.query(LearningContent)
            .filter(
                LearningContent.topic_id == topic.id,
                LearningContent.resource_type == item["resource_type"]
            )
            .first()
        )


        if existing:

            existing.title = item["title"]

            existing.description = item["description"]

            existing.content_text = item["content_text"]

            existing.resource_url = item["resource_url"]

            existing.content_order = item["content_order"]

            existing.is_active = True


        else:

            content = LearningContent(

                topic_id=topic.id,

                resource_type=item["resource_type"],

                title=item["title"],

                description=item["description"],

                content_text=item["content_text"],

                resource_url=item["resource_url"],

                content_order=item["content_order"],

                uploaded_by=None,

                is_active=True
            )


            db.add(content)


    db.commit()


    # =========================================================
    # VERIFY
    # =========================================================

    saved_contents = (
        db.query(LearningContent)
        .filter(
            LearningContent.topic_id == topic.id
        )
        .order_by(
            LearningContent.content_order
        )
        .all()
    )


    print("")
    print("========================================")
    print(" TOPIC 1 LEARNING CONTENT CREATED")
    print("========================================")
    print("")

    print(
        f"Topic: {topic.title}"
    )

    print(
        f"Total Learning Methods: {len(saved_contents)}"
    )

    print("")


    for content in saved_contents:

        print(
            f"{content.content_order}. "
            f"{content.resource_type.upper()} "
            f"- {content.title}"
        )


    print("")


except Exception as error:

    db.rollback()

    print("")
    print("CONTENT SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()