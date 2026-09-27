import json

from app.db.database import SessionLocal

from app.models.user import User
from app.models.topic import Topic
from app.models.note import Note, NoteSection


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
    # FIND ACTIVE NOTE
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

        raise Exception(
            "Rich notes not found."
        )


    # =========================================================
    # REMOVE OLD CHECKPOINTS
    # =========================================================

    (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id,
            NoteSection.section_type == "checkpoint"
        )
        .delete(
            synchronize_session=False
        )
    )


    # =========================================================
    # REORDER EXISTING CONTENT
    # =========================================================

    existing_sections = (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id
        )
        .all()
    )


    order_map = {

        "A Morning Full of Physics":
            10,

        "So, What Exactly Is Physics?":
            20,

        "Example 1 — What Happens When You Kick a Football?":
            30,

        "Physics Is Hidden Inside the Technology Around You":
            40,

        "Example 2 — How Can a Rocket Move in Space?":
            50,

        "Where Will You Use Physics in Engineering?":
            60,

        "What Should You Remember?":
            80
    }


    for section in existing_sections:

        if section.heading in order_map:

            section.section_order = (
                order_map[
                    section.heading
                ]
            )


    # =========================================================
    # CHECKPOINT 1
    # WALKING / FRICTION
    # =========================================================

    checkpoint_1 = NoteSection(

        note_id=
            note.id,

        section_order=
            15,

        section_type=
            "checkpoint",

        heading=
            "Quick Check 1 — Why Can You Walk Without Slipping?",

        body=
            "Think about the morning walking example.",

        media_url=
            None,

        media_type=
            None,

        caption=
            None,

        alt_text=
            None,

        interactive_data=
            json.dumps(
                {

                    "question":
                        "When you walk normally on the floor, which force mainly prevents your foot from simply sliding backward?",

                    "options": [

                        "Friction",

                        "Gravity",

                        "Magnetism",

                        "Air resistance"

                    ],

                    "answer":
                        "Friction",

                    "explanation":
                        "Your foot pushes backward against the ground. Friction between your foot and the floor allows the ground to provide a forward force, helping you move ahead."

                }
            ),

        is_active=
            True
    )


    # =========================================================
    # CHECKPOINT 2
    # FOOTBALL
    # =========================================================

    checkpoint_2 = NoteSection(

        note_id=
            note.id,

        section_order=
            35,

        section_type=
            "checkpoint",

        heading=
            "Quick Check 2 — Why Does the Football Follow a Curved Path?",

        body=
            "Use the animated football example you just observed.",

        media_url=
            None,

        media_type=
            None,

        caption=
            None,

        alt_text=
            None,

        interactive_data=
            json.dumps(
                {

                    "question":
                        "After a football is kicked into the air, why does its path become curved?",

                    "options": [

                        "Forward motion continues while gravity pulls it downward",

                        "The ball suddenly loses all forward motion",

                        "Magnetism pulls the ball toward the ground",

                        "The air pushes the ball upward continuously"

                    ],

                    "answer":
                        "Forward motion continues while gravity pulls it downward",

                    "explanation":
                        "The kick gives the ball forward velocity. After it leaves the foot, the ball continues moving forward while gravity continuously accelerates it downward. These two motions combine to create a curved projectile path."

                }
            ),

        is_active=
            True
    )


    # =========================================================
    # CHECKPOINT 3
    # ROCKET
    # =========================================================

    checkpoint_3 = NoteSection(

        note_id=
            note.id,

        section_order=
            55,

        section_type=
            "checkpoint",

        heading=
            "Quick Check 3 — Why Does a Rocket Move Upward?",

        body=
            "Think about the action-reaction animation.",

        media_url=
            None,

        media_type=
            None,

        caption=
            None,

        alt_text=
            None,

        interactive_data=
            json.dumps(
                {

                    "question":
                        "A rocket engine throws exhaust gases downward at high speed. What causes the rocket to accelerate upward?",

                    "options": [

                        "An equal and opposite reaction force",

                        "The rocket pushes against the surrounding air",

                        "Gravity changes direction",

                        "The exhaust gases pull the rocket upward"

                    ],

                    "answer":
                        "An equal and opposite reaction force",

                    "explanation":
                        "The engine accelerates exhaust gases downward. According to Newton's Third Law, the gases exert an equal and opposite force on the rocket. This upward force is called thrust."

                }
            ),

        is_active=
            True
    )


    # =========================================================
    # CHECKPOINT 4
    # INERTIA
    # =========================================================

    checkpoint_4 = NoteSection(

        note_id=
            note.id,

        section_order=
            70,

        section_type=
            "checkpoint",

        heading=
            "Quick Check 4 — Why Does a Passenger Move Forward When a Car Stops Suddenly?",

        body=
            "Connect this everyday situation to Newton's First Law.",

        media_url=
            None,

        media_type=
            None,

        caption=
            None,

        alt_text=
            None,

        interactive_data=
            json.dumps(
                {

                    "question":
                        "A moving car suddenly stops, but the passenger's body tends to continue moving forward. Which concept explains this?",

                    "options": [

                        "Inertia",

                        "Refraction",

                        "Electromagnetism",

                        "Buoyancy"

                    ],

                    "answer":
                        "Inertia",

                    "explanation":
                        "A moving body tends to remain in motion unless an external force changes its state. The passenger's body therefore tends to continue moving forward when the vehicle suddenly stops. This is inertia and is explained by Newton's First Law."

                }
            ),

        is_active=
            True
    )


    # =========================================================
    # ADD CHECKPOINTS
    # =========================================================

    db.add_all(
        [
            checkpoint_1,
            checkpoint_2,
            checkpoint_3,
            checkpoint_4
        ]
    )


    db.commit()


    # =========================================================
    # VERIFY
    # =========================================================

    sections = (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id
        )
        .order_by(
            NoteSection.section_order
        )
        .all()
    )


    print("")
    print("==========================================")
    print(" TOPIC 1 CHECKPOINTS UPDATED SUCCESSFULLY")
    print("==========================================")
    print("")


    for section in sections:

        print(
            f"{section.section_order}. "
            f"{section.section_type.upper()} "
            f"- {section.heading}"
        )


    print("")

    print("Total checkpoints: 4")

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("CHECKPOINT UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()