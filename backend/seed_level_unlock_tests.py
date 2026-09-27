import json

from sqlalchemy import func

from app.db.database import SessionLocal

from app.models.user import User
from app.models.course import Course
from app.models.year import AcademicYear
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic

from app.models.level_test import (
    StudentLevelProgress,
    LevelTestQuestion,
    LevelTestAttempt,
    LevelTestAnswer
)


db = SessionLocal()


try:

    # ============================================================
    # FIND PHYSICS SUBJECT USING OUR KNOWN TOPICS
    # ============================================================

    topic1 = (
        db.query(Topic)
        .filter(Topic.id == 1)
        .first()
    )


    if not topic1:

        raise Exception(
            "Topic 1 not found. Cannot identify Physics subject."
        )


    subject_id = topic1.subject_id


    # ============================================================
    # FIND LEVELS SAFELY BY NAME + SUBJECT
    # ============================================================

    def get_level(level_name):

        level = (
            db.query(Level)
            .filter(
                Level.subject_id == subject_id,
                func.lower(Level.name) == level_name.lower()
            )
            .first()
        )


        if not level:

            raise Exception(
                f"Level '{level_name}' not found "
                f"for subject ID {subject_id}."
            )


        return level


    entry = get_level("Entry")
    basics = get_level("Basics")
    intermediate = get_level("Intermediate")
    pro = get_level("Pro")


    # ============================================================
    # VERIFY TOPICS
    # ============================================================

    topics = {}


    for topic_id in range(1, 9):

        topic = (
            db.query(Topic)
            .filter(
                Topic.id == topic_id,
                Topic.subject_id == subject_id
            )
            .first()
        )


        if not topic:

            raise Exception(
                f"Topic ID {topic_id} not found "
                f"inside subject ID {subject_id}."
            )


        topics[topic_id] = topic


    # ============================================================
    # QUESTION DATA
    # ============================================================

    tests = [

        # ========================================================
        # ENTRY → BASICS
        # Topics 1 and 2
        # ========================================================

        {
            "source_level": entry,
            "target_level": basics,

            "questions": [

                {
                    "order": 1,
                    "topic_id": 1,

                    "question":
                        "What is Physics mainly concerned with studying?",

                    "options": [
                        "Matter, energy, motion and their interactions",
                        "Only living organisms",
                        "Only historical events",
                        "Only computer programming"
                    ],

                    "answer":
                        "Matter, energy, motion and their interactions",

                    "concept_gap":
                        "Meaning and Scope of Physics",

                    "explanation":
                        "Physics studies matter, energy, motion, forces and the interactions that explain how physical systems behave."
                },


                {
                    "order": 2,
                    "topic_id": 1,

                    "question":
                        "Which situation is an example of Physics in everyday life?",

                    "options": [
                        "Braking a moving bicycle",
                        "Spelling a word",
                        "Memorising a poem",
                        "Writing a historical date"
                    ],

                    "answer":
                        "Braking a moving bicycle",

                    "concept_gap":
                        "Real-World Applications of Physics",

                    "explanation":
                        "Braking involves motion, forces, friction and energy, all of which are physical concepts."
                },


                {
                    "order": 3,
                    "topic_id": 1,

                    "question":
                        "Which Physics concept helps explain why a football changes direction after being kicked?",

                    "options": [
                        "Force",
                        "Temperature only",
                        "Colour",
                        "Density only"
                    ],

                    "answer":
                        "Force",

                    "concept_gap":
                        "Force and Motion",

                    "explanation":
                        "A kick applies a force to the football. A force can change the speed or direction of an object's motion."
                },


                {
                    "order": 4,
                    "topic_id": 1,

                    "question":
                        "Which technology depends strongly on principles of Physics?",

                    "options": [
                        "Electric motor",
                        "Grammar dictionary",
                        "Printed calendar",
                        "Alphabet chart"
                    ],

                    "answer":
                        "Electric motor",

                    "concept_gap":
                        "Physics in Technology",

                    "explanation":
                        "Electric motors operate through electricity, magnetism, force and motion, all of which are Physics concepts."
                },


                {
                    "order": 5,
                    "topic_id": 1,

                    "question":
                        "Why is Physics important in engineering?",

                    "options": [
                        "It helps predict and understand how physical systems behave",
                        "It removes the need for measurements",
                        "It guarantees every design works without testing",
                        "It is used only to name materials"
                    ],

                    "answer":
                        "It helps predict and understand how physical systems behave",

                    "concept_gap":
                        "Physics and Engineering",

                    "explanation":
                        "Engineering uses Physics to analyse forces, motion, energy, electricity, heat and many other behaviours before designing systems."
                },


                {
                    "order": 6,
                    "topic_id": 2,

                    "question":
                        "A student walks 100 m east and then 100 m west back to the starting point. What is the final displacement?",

                    "options": [
                        "0 m",
                        "100 m",
                        "200 m",
                        "50 m"
                    ],

                    "answer":
                        "0 m",

                    "concept_gap":
                        "Distance vs Displacement",

                    "explanation":
                        "Displacement depends only on the change from initial to final position. Since the student returns to the starting point, displacement is zero."
                },


                {
                    "order": 7,
                    "topic_id": 2,

                    "question":
                        "A car travels 150 km in 3 hours. What is its average speed?",

                    "options": [
                        "50 km/h",
                        "450 km/h",
                        "153 km/h",
                        "147 km/h"
                    ],

                    "answer":
                        "50 km/h",

                    "concept_gap":
                        "Average Speed",

                    "explanation":
                        "Average speed = Total Distance / Total Time = 150 / 3 = 50 km/h."
                },


                {
                    "order": 8,
                    "topic_id": 2,

                    "question":
                        "Which quantity requires both magnitude and direction?",

                    "options": [
                        "Velocity",
                        "Distance",
                        "Speed",
                        "Time"
                    ],

                    "answer":
                        "Velocity",

                    "concept_gap":
                        "Speed vs Velocity",

                    "explanation":
                        "Velocity is a vector quantity because it includes both magnitude and direction. Speed has magnitude only."
                },


                {
                    "order": 9,
                    "topic_id": 2,

                    "question":
                        "Two cars move at 60 km/h, one east and one west. Which statement is correct?",

                    "options": [
                        "They have the same speed but different velocities",
                        "They have different speeds and the same velocity",
                        "They have the same velocity",
                        "Neither car has velocity"
                    ],

                    "answer":
                        "They have the same speed but different velocities",

                    "concept_gap":
                        "Direction in Velocity",

                    "explanation":
                        "Their speed magnitudes are equal, but their directions are opposite. Therefore their velocities are different."
                },


                {
                    "order": 10,
                    "topic_id": 2,

                    "question":
                        "Which formula correctly calculates average speed?",

                    "options": [
                        "Total Distance / Total Time",
                        "Total Time / Total Distance",
                        "Distance × Time",
                        "Distance + Time"
                    ],

                    "answer":
                        "Total Distance / Total Time",

                    "concept_gap":
                        "Speed Formula",

                    "explanation":
                        "Average speed is calculated by dividing the total distance travelled by the total time taken."
                }
            ]
        },


        # ========================================================
        # BASICS → INTERMEDIATE
        # Topics 3, 4 and 5
        # ========================================================

        {
            "source_level": basics,
            "target_level": intermediate,

            "questions": [

                {
                    "order": 1,
                    "topic_id": 3,

                    "question":
                        "A book rests on a table. Gravity pulls downward while the table provides an equal upward force. What is the net force?",

                    "options": [
                        "0 N",
                        "Equal to gravity",
                        "Twice the weight",
                        "Infinite"
                    ],

                    "answer":
                        "0 N",

                    "concept_gap":
                        "Balanced Forces",

                    "explanation":
                        "The upward and downward forces are equal and opposite, so they cancel and the net force is zero."
                },


                {
                    "order": 2,
                    "topic_id": 3,

                    "question":
                        "Why does a passenger tend to move forward when a moving bus suddenly stops?",

                    "options": [
                        "Inertia",
                        "Magnetism",
                        "Refraction",
                        "Electrical resistance"
                    ],

                    "answer":
                        "Inertia",

                    "concept_gap":
                        "Newton's First Law",

                    "explanation":
                        "The passenger's body tends to maintain its existing state of motion. This resistance to a change in motion is inertia."
                },


                {
                    "order": 3,
                    "topic_id": 3,

                    "question":
                        "A 4 kg object accelerates at 3 m/s². What net force acts on it?",

                    "options": [
                        "12 N",
                        "7 N",
                        "1.33 N",
                        "24 N"
                    ],

                    "answer":
                        "12 N",

                    "concept_gap":
                        "Newton's Second Law",

                    "explanation":
                        "Using F = ma, F = 4 × 3 = 12 N."
                },


                {
                    "order": 4,
                    "topic_id": 4,

                    "question":
                        "You push a rigid wall but it does not move. What mechanical work is done on the wall?",

                    "options": [
                        "0 J",
                        "Maximum work",
                        "Equal to the force applied",
                        "Cannot be determined because force exists"
                    ],

                    "answer":
                        "0 J",

                    "concept_gap":
                        "Mechanical Work",

                    "explanation":
                        "Mechanical work requires displacement. Since the wall has zero displacement, W = F × 0 = 0."
                },


                {
                    "order": 5,
                    "topic_id": 4,

                    "question":
                        "A 2 kg object moves at 4 m/s. What is its kinetic energy?",

                    "options": [
                        "16 J",
                        "8 J",
                        "4 J",
                        "32 J"
                    ],

                    "answer":
                        "16 J",

                    "concept_gap":
                        "Kinetic Energy",

                    "explanation":
                        "KE = 1/2 mv² = 1/2 × 2 × 4² = 16 J."
                },


                {
                    "order": 6,
                    "topic_id": 4,

                    "question":
                        "A machine performs 600 J of work in 3 seconds. What is its power?",

                    "options": [
                        "200 W",
                        "1800 W",
                        "603 W",
                        "20 W"
                    ],

                    "answer":
                        "200 W",

                    "concept_gap":
                        "Power",

                    "explanation":
                        "Power = Work / Time = 600 / 3 = 200 W."
                },


                {
                    "order": 7,
                    "topic_id": 5,

                    "question":
                        "A 5 kg object moves at 4 m/s. What is its momentum?",

                    "options": [
                        "20 kg·m/s",
                        "9 kg·m/s",
                        "1.25 kg·m/s",
                        "40 kg·m/s"
                    ],

                    "answer":
                        "20 kg·m/s",

                    "concept_gap":
                        "Linear Momentum",

                    "explanation":
                        "Momentum p = mv = 5 × 4 = 20 kg·m/s."
                },


                {
                    "order": 8,
                    "topic_id": 5,

                    "question":
                        "Why do airbags help reduce the average force on a passenger during a collision?",

                    "options": [
                        "They increase the time over which momentum changes",
                        "They increase passenger mass",
                        "They remove momentum instantly",
                        "They increase vehicle velocity"
                    ],

                    "answer":
                        "They increase the time over which momentum changes",

                    "concept_gap":
                        "Impulse and Impact Force",

                    "explanation":
                        "For the same change in momentum, increasing the stopping time reduces the average force."
                },


                {
                    "order": 9,
                    "topic_id": 5,

                    "question":
                        "In an isolated collision with negligible external force, which quantity is conserved?",

                    "options": [
                        "Total momentum",
                        "Each object's velocity",
                        "Each object's kinetic energy in every collision",
                        "Each object's mass times acceleration"
                    ],

                    "answer":
                        "Total momentum",

                    "concept_gap":
                        "Conservation of Momentum",

                    "explanation":
                        "For an isolated system, the total momentum before a collision equals the total momentum after the collision."
                },


                {
                    "order": 10,
                    "topic_id": 5,

                    "question":
                        "Two objects collide and stick together after impact. What type of collision is this?",

                    "options": [
                        "Perfectly inelastic collision",
                        "Perfectly elastic collision",
                        "No collision",
                        "Uniform circular motion"
                    ],

                    "answer":
                        "Perfectly inelastic collision",

                    "concept_gap":
                        "Collision Types",

                    "explanation":
                        "When objects stick together and move with a common velocity after impact, the collision is perfectly inelastic."
                }
            ]
        },


        # ========================================================
        # INTERMEDIATE → PRO
        # Topics 6, 7 and 8
        # ========================================================

        {
            "source_level": intermediate,
            "target_level": pro,

            "questions": [

                {
                    "order": 1,
                    "topic_id": 6,

                    "question":
                        "A source completes 200 vibrations in one second. What is its frequency?",

                    "options": [
                        "200 Hz",
                        "20 Hz",
                        "2 Hz",
                        "0.005 Hz"
                    ],

                    "answer":
                        "200 Hz",

                    "concept_gap":
                        "Frequency",

                    "explanation":
                        "Frequency is the number of complete cycles per second. Therefore 200 cycles per second equals 200 Hz."
                },


                {
                    "order": 2,
                    "topic_id": 6,

                    "question":
                        "A wave has frequency 10 Hz and wavelength 3 m. What is its wave speed?",

                    "options": [
                        "30 m/s",
                        "13 m/s",
                        "3.33 m/s",
                        "0.3 m/s"
                    ],

                    "answer":
                        "30 m/s",

                    "concept_gap":
                        "Wave Speed",

                    "explanation":
                        "Wave speed v = fλ = 10 × 3 = 30 m/s."
                },


                {
                    "order": 3,
                    "topic_id": 6,

                    "question":
                        "Why can sound not travel through a perfect vacuum?",

                    "options": [
                        "There are no particles available to transfer the vibration",
                        "Sound needs gravity",
                        "Vacuum contains too much resistance",
                        "Frequency automatically becomes infinite"
                    ],

                    "answer":
                        "There are no particles available to transfer the vibration",

                    "concept_gap":
                        "Sound as a Mechanical Wave",

                    "explanation":
                        "Sound requires particles in a material medium to transfer vibration energy. A perfect vacuum contains no such particles."
                },


                {
                    "order": 4,
                    "topic_id": 7,

                    "question":
                        "12 coulombs of charge pass through a conductor in 3 seconds. What is the current?",

                    "options": [
                        "4 A",
                        "36 A",
                        "9 A",
                        "0.25 A"
                    ],

                    "answer":
                        "4 A",

                    "concept_gap":
                        "Electric Current",

                    "explanation":
                        "Current I = Q/t = 12/3 = 4 A."
                },


                {
                    "order": 5,
                    "topic_id": 7,

                    "question":
                        "A 12 V source is connected across a 4 Ω resistor. What current flows?",

                    "options": [
                        "3 A",
                        "48 A",
                        "8 A",
                        "0.33 A"
                    ],

                    "answer":
                        "3 A",

                    "concept_gap":
                        "Ohm's Law",

                    "explanation":
                        "Using I = V/R, I = 12/4 = 3 A."
                },


                {
                    "order": 6,
                    "topic_id": 7,

                    "question":
                        "Why are household appliances generally connected in parallel?",

                    "options": [
                        "Each appliance can operate independently across the supply",
                        "Parallel circuits have zero current",
                        "Parallel circuits have no voltage",
                        "All appliances must switch off together"
                    ],

                    "answer":
                        "Each appliance can operate independently across the supply",

                    "concept_gap":
                        "Parallel Circuits",

                    "explanation":
                        "Parallel branches receive the supply voltage independently, allowing devices to operate and switch separately."
                },


                {
                    "order": 7,
                    "topic_id": 8,

                    "question":
                        "What is produced around a conductor when electric current flows through it?",

                    "options": [
                        "A magnetic field",
                        "A gravitational vacuum",
                        "Zero resistance",
                        "A sound wave only"
                    ],

                    "answer":
                        "A magnetic field",

                    "concept_gap":
                        "Magnetic Effect of Electric Current",

                    "explanation":
                        "Moving electric charge produces a magnetic field around the current-carrying conductor."
                },


                {
                    "order": 8,
                    "topic_id": 8,

                    "question":
                        "Which change can generally make an electromagnet stronger?",

                    "options": [
                        "Increasing current through the coil",
                        "Removing all current",
                        "Using zero coil turns",
                        "Opening the circuit permanently"
                    ],

                    "answer":
                        "Increasing current through the coil",

                    "concept_gap":
                        "Electromagnet Strength",

                    "explanation":
                        "A larger current generally creates a stronger magnetic field. More coil turns and a suitable iron core can also strengthen the electromagnet."
                },


                {
                    "order": 9,
                    "topic_id": 8,

                    "question":
                        "What is the main energy conversion in an electric motor?",

                    "options": [
                        "Electrical energy to mechanical energy",
                        "Mechanical energy to electrical energy",
                        "Thermal energy to nuclear energy",
                        "Sound energy to mass"
                    ],

                    "answer":
                        "Electrical energy to mechanical energy",

                    "concept_gap":
                        "Electric Motor Principle",

                    "explanation":
                        "An electric motor uses electromagnetic forces to convert electrical energy into mechanical motion."
                },


                {
                    "order": 10,
                    "topic_id": 8,

                    "question":
                        "Which device mainly converts mechanical energy into electrical energy using electromagnetic induction?",

                    "options": [
                        "Generator",
                        "Electric motor",
                        "Resistor",
                        "Switch"
                    ],

                    "answer":
                        "Generator",

                    "concept_gap":
                        "Electromagnetic Induction and Generators",

                    "explanation":
                        "A generator uses changing magnetic conditions to induce electrical voltage, converting mechanical energy into electrical energy."
                }
            ]
        }
    ]


    # ============================================================
    # UPSERT QUESTIONS
    # ============================================================

    created_count = 0
    updated_count = 0


    for test in tests:

        source_level = test["source_level"]
        target_level = test["target_level"]


        for item in test["questions"]:

            question = (
                db.query(LevelTestQuestion)
                .filter(
                    LevelTestQuestion.subject_id == subject_id,
                    LevelTestQuestion.source_level_id == source_level.id,
                    LevelTestQuestion.target_level_id == target_level.id,
                    LevelTestQuestion.question_order == item["order"]
                )
                .first()
            )


            if not question:

                question = LevelTestQuestion(

                    subject_id=
                        subject_id,

                    source_level_id=
                        source_level.id,

                    target_level_id=
                        target_level.id,

                    topic_id=
                        item["topic_id"],

                    question_order=
                        item["order"],

                    question_text=
                        item["question"],

                    options_json=
                        json.dumps(
                            item["options"],
                            ensure_ascii=False
                        ),

                    correct_answer=
                        item["answer"],

                    explanation=
                        item["explanation"],

                    concept_gap=
                        item["concept_gap"],

                    is_active=
                        True
                )


                db.add(question)

                created_count += 1


            else:

                question.topic_id = (
                    item["topic_id"]
                )

                question.question_text = (
                    item["question"]
                )

                question.options_json = json.dumps(
                    item["options"],
                    ensure_ascii=False
                )

                question.correct_answer = (
                    item["answer"]
                )

                question.explanation = (
                    item["explanation"]
                )

                question.concept_gap = (
                    item["concept_gap"]
                )

                question.is_active = True

                updated_count += 1


    db.commit()


    # ============================================================
    # VERIFY
    # ============================================================

    entry_count = (
        db.query(LevelTestQuestion)
        .filter(
            LevelTestQuestion.subject_id == subject_id,
            LevelTestQuestion.source_level_id == entry.id,
            LevelTestQuestion.target_level_id == basics.id,
            LevelTestQuestion.is_active == True
        )
        .count()
    )


    basics_count = (
        db.query(LevelTestQuestion)
        .filter(
            LevelTestQuestion.subject_id == subject_id,
            LevelTestQuestion.source_level_id == basics.id,
            LevelTestQuestion.target_level_id == intermediate.id,
            LevelTestQuestion.is_active == True
        )
        .count()
    )


    intermediate_count = (
        db.query(LevelTestQuestion)
        .filter(
            LevelTestQuestion.subject_id == subject_id,
            LevelTestQuestion.source_level_id == intermediate.id,
            LevelTestQuestion.target_level_id == pro.id,
            LevelTestQuestion.is_active == True
        )
        .count()
    )


    total_count = (
        db.query(LevelTestQuestion)
        .filter(
            LevelTestQuestion.subject_id == subject_id,
            LevelTestQuestion.is_active == True
        )
        .count()
    )


    print("")
    print("==============================================")
    print(" LEVEL UNLOCK TEST QUESTIONS SEEDED")
    print("==============================================")
    print("")

    print(
        f"Subject ID            : {subject_id}"
    )

    print(
        f"Entry Level ID        : {entry.id}"
    )

    print(
        f"Basics Level ID       : {basics.id}"
    )

    print(
        f"Intermediate Level ID : {intermediate.id}"
    )

    print(
        f"Pro Level ID          : {pro.id}"
    )

    print("")

    print(
        f"Created               : {created_count}"
    )

    print(
        f"Updated               : {updated_count}"
    )

    print("")

    print(
        f"Entry -> Basics       : {entry_count}/10"
    )

    print(
        f"Basics -> Intermediate: {basics_count}/10"
    )

    print(
        f"Intermediate -> Pro   : {intermediate_count}/10"
    )

    print("")

    print(
        f"TOTAL ACTIVE QUESTIONS: {total_count}"
    )

    print("")

    print(
        "PASS RULE             : 8 / 10"
    )

    print(
        "WRONG ANSWER FEEDBACK : Concept Gap + Explanation"
    )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("LEVEL TEST SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()