from app.db.database import Base, SessionLocal, engine

from app.models.course import Course
from app.models.year import AcademicYear
from app.models.subject import Subject
from app.models.level import Level
from app.models.topic import Topic


Base.metadata.create_all(bind=engine)

db = SessionLocal()


try:

    # =========================================================
    # COURSE
    # =========================================================

    course = (
        db.query(Course)
        .filter(Course.code == "BE")
        .first()
    )

    if not course:
        course = Course(
            name="Bachelor of Engineering",
            code="BE"
        )

        db.add(course)
        db.commit()
        db.refresh(course)


    # =========================================================
    # YEAR
    # =========================================================

    academic_year = (
        db.query(AcademicYear)
        .filter(
            AcademicYear.course_id == course.id,
            AcademicYear.year_number == 1
        )
        .first()
    )

    if not academic_year:
        academic_year = AcademicYear(
            year_number=1,
            name="1st Year",
            course_id=course.id
        )

        db.add(academic_year)
        db.commit()
        db.refresh(academic_year)


    # =========================================================
    # SUBJECT
    # =========================================================

    subject = (
        db.query(Subject)
        .filter(
            Subject.course_id == course.id,
            Subject.year_id == academic_year.id,
            Subject.code == "PHY101"
        )
        .first()
    )

    if not subject:
        subject = Subject(
            name="Physics",
            code="PHY101",
            course_id=course.id,
            year_id=academic_year.id
        )

        db.add(subject)
        db.commit()
        db.refresh(subject)


    # =========================================================
    # LEVELS
    # =========================================================

    level_data = [
        {
            "name": "Entry",
            "order": 1,
            "default_unlocked": True,
            "score_required": 0
        },
        {
            "name": "Basics",
            "order": 2,
            "default_unlocked": False,
            "score_required": 8
        },
        {
            "name": "Intermediate",
            "order": 3,
            "default_unlocked": False,
            "score_required": 8
        },
        {
            "name": "Pro",
            "order": 4,
            "default_unlocked": False,
            "score_required": 8
        }
    ]


    levels = {}


    for item in level_data:

        level = (
            db.query(Level)
            .filter(
                Level.subject_id == subject.id,
                Level.level_order == item["order"]
            )
            .first()
        )

        if not level:

            level = Level(
                name=item["name"],
                level_order=item["order"],
                subject_id=subject.id,
                is_default_unlocked=item["default_unlocked"],
                unlock_score_required=item["score_required"]
            )

            db.add(level)
            db.commit()
            db.refresh(level)

        levels[item["name"]] = level


    # =========================================================
    # PHYSICS TOPICS
    # =========================================================

    topics = [

        # -----------------------------------------------------
        # ENTRY
        # -----------------------------------------------------

        {
            "level": "Entry",
            "order": 1,
            "title": "Why Physics? & Real-World Applications",
            "description":
                "Understand why physics matters and discover how physics "
                "is used in vehicles, mobile phones, buildings, sports, "
                "medicine, satellites and everyday technology.",
            "visualization":
                "Animated Real-World Physics Explorer",
            "game":
                "Find the Physics Around You"
        },

        {
            "level": "Entry",
            "order": 2,
            "title": "Motion, Distance, Speed & Velocity",
            "description":
                "Learn how objects move and understand distance, "
                "displacement, speed and velocity using interactive motion.",
            "visualization":
                "Interactive Moving Car Simulation",
            "game":
                "Speed and Velocity Challenge"
        },


        # -----------------------------------------------------
        # BASICS
        # -----------------------------------------------------

        {
            "level": "Basics",
            "order": 1,
            "title": "Forces & Newton's Laws",
            "description":
                "Explore force, inertia, acceleration, action and reaction "
                "through practical and interactive examples.",
            "visualization":
                "Force Vector and Motion Simulator",
            "game":
                "Push, Pull and Balance Challenge"
        },

        {
            "level": "Basics",
            "order": 2,
            "title": "Work, Energy & Power",
            "description":
                "Understand work, kinetic energy, potential energy, "
                "energy conversion and power.",
            "visualization":
                "Interactive Energy Conversion Simulator",
            "game":
                "Energy Mission"
        },

        {
            "level": "Basics",
            "order": 3,
            "title": "Momentum & Collisions",
            "description":
                "Learn momentum, impulse and collision behaviour "
                "using moving objects with different masses and velocities.",
            "visualization":
                "Interactive Collision Simulator",
            "game":
                "Collision Prediction Challenge"
        },


        # -----------------------------------------------------
        # INTERMEDIATE
        # -----------------------------------------------------

        {
            "level": "Intermediate",
            "order": 1,
            "title": "Waves, Sound & Vibrations",
            "description":
                "Explore wave motion, amplitude, frequency, wavelength, "
                "sound and vibrations.",
            "visualization":
                "Interactive Wave Generator",
            "game":
                "Match the Frequency"
        },

        {
            "level": "Intermediate",
            "order": 2,
            "title": "Electricity & Electric Circuits",
            "description":
                "Understand voltage, current, resistance and basic "
                "electrical circuits through interactive circuit building.",
            "visualization":
                "Virtual Circuit Builder",
            "game":
                "Light the Bulb Challenge"
        },

        {
            "level": "Intermediate",
            "order": 3,
            "title": "Magnetism & Electromagnetism",
            "description":
                "Explore magnetic fields, magnetic forces and "
                "electromagnetism through interactive models.",
            "visualization":
                "3D Magnetic Field Explorer",
            "game":
                "Build an Electromagnet"
        },


        # -----------------------------------------------------
        # PRO
        # -----------------------------------------------------

        {
            "level": "Pro",
            "order": 1,
            "title": "Light & Optics",
            "description":
                "Explore reflection, refraction, mirrors and lenses "
                "with interactive light-ray visualization.",
            "visualization":
                "Interactive Ray Optics Lab",
            "game":
                "Guide the Light Beam"
        },

        {
            "level": "Pro",
            "order": 2,
            "title": "Modern Physics",
            "description":
                "Explore atoms, photons, nuclear physics and introductory "
                "modern physics concepts through visual models.",
            "visualization":
                "Interactive Atomic Explorer",
            "game":
                "Atomic Physics Challenge"
        }
    ]


    # =========================================================
    # INSERT TOPICS
    # =========================================================

    for item in topics:

        level = levels[item["level"]]

        existing_topic = (
            db.query(Topic)
            .filter(
                Topic.level_id == level.id,
                Topic.topic_order == item["order"]
            )
            .first()
        )

        if not existing_topic:

            topic = Topic(
                title=item["title"],
                description=item["description"],
                topic_order=item["order"],
                subject_id=subject.id,
                level_id=level.id,
                visualization_type=item["visualization"],
                game_type=item["game"]
            )

            db.add(topic)


    db.commit()


    # =========================================================
    # RESULT
    # =========================================================

    total_topics = (
        db.query(Topic)
        .filter(Topic.subject_id == subject.id)
        .count()
    )


    print("")
    print("=======================================")
    print(" PHYSICS DEMO DATA CREATED SUCCESSFULLY")
    print("=======================================")

    print(f"Course  : {course.name}")
    print(f"Year    : {academic_year.name}")
    print(f"Subject : {subject.name}")
    print(f"Topics  : {total_topics}")

    print("")
    print("Levels:")

    for name in [
        "Entry",
        "Basics",
        "Intermediate",
        "Pro"
    ]:

        level = levels[name]

        status = (
            "UNLOCKED"
            if level.is_default_unlocked
            else "LOCKED"
        )

        print(
            f"- {name}: {status}"
        )

    print("")


except Exception as error:

    db.rollback()

    print("")
    print("SEED ERROR:")
    print(error)
    print("")


finally:

    db.close()