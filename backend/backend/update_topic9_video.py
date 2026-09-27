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
    # TOPIC 9
    # =========================================================

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


    # =========================================================
    # VERIFIED ENGLISH VIDEO
    # =========================================================

    video_title = (
        "Refraction of Light - Geometric Optics"
    )


    video_description = (
        "English Physics lesson covering reflection, refraction, "
        "Snell's Law, refractive index, critical angle and "
        "total internal reflection."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=ON1QGqB6vxg"
    )


    learning_guide = """
BEFORE YOU WATCH

This video is in ENGLISH.

You already studied:

• Light
• Reflection
• Refraction
• Refractive index
• Lenses
• Real and virtual images
• Dispersion

through the Rich Notes.


WHAT TO FOCUS ON

1. Law of Reflection

2. Refraction of Light

3. Refractive Index

4. Snell's Law

5. Speed of Light in Different Materials

6. Critical Angle

7. Total Internal Reflection


REFLECTION

When light hits a surface and returns
into the same medium:

Reflection occurs.


LAW OF REFLECTION

Angle of Incidence
=
Angle of Reflection


i = r


IMPORTANT

Angles are measured relative
to the normal.


REFRACTION

When light travels from one medium
into another medium,
its speed can change.

Because of this,
its direction can also change.

This bending is called:

REFRACTION


EXAMPLE

Air
→ Water


Air
→ Glass


REFRACTIVE INDEX

Refractive index tells us
how much light slows down
inside a material.


FORMULA

n = c / v


Where:

n = Refractive Index

c = Speed of light in vacuum

v = Speed of light in material


EXAMPLE

c = 3 × 10^8 m/s

v = 2 × 10^8 m/s


n = c / v

n = 1.5


SNELL'S LAW

Refraction can be calculated using:

n₁ sin θ₁
=
n₂ sin θ₂


Where:

n₁ = Refractive index of first medium

n₂ = Refractive index of second medium

θ₁ = Incident angle

θ₂ = Refracted angle


IMPORTANT IDEA

Entering a higher refractive-index medium:

Light generally bends
toward the normal.


Entering a lower refractive-index medium:

Light generally bends
away from the normal.


SPEED OF LIGHT

Light travels fastest in vacuum.

Approximately:

3 × 10^8 m/s


Inside materials such as:

• Water
• Glass

light travels more slowly.


TOTAL INTERNAL REFLECTION

Under suitable conditions,
light travelling from a higher refractive-index medium
toward a lower-index medium
can reflect completely back inside.


This is called:

TOTAL INTERNAL REFLECTION


CRITICAL ANGLE

The critical angle is the incident angle
for which the refracted ray travels
along the boundary.


If incident angle becomes greater
than the critical angle:

Total internal reflection can occur.


REAL-WORLD APPLICATION

FIBER OPTICS

Light can travel through an optical fibre
using repeated total internal reflection.


Used in:

• Internet communication
• Telecommunications
• Medical endoscopy
• Optical sensors


CONNECT WITH OUR RICH NOTES

Our notes also cover lenses.


CONVEX LENS

Converging lens.

Parallel rays can converge
toward a focal point.


CONCAVE LENS

Diverging lens.

Parallel rays spread apart.


REAL IMAGE

Light rays actually converge.

Can generally be projected
onto a screen.


VIRTUAL IMAGE

Light rays only appear
to originate from the image position.


SELF CHECK 1

Incident angle:

30°


For reflection:

Reflection angle = 30°


SELF CHECK 2

Vacuum speed:

3 × 10^8 m/s


Material speed:

2 × 10^8 m/s


n = c / v

n = 1.5


SELF CHECK 3

Which law describes refraction?

Snell's Law.


SELF CHECK 4

What principle allows light
to remain trapped inside optical fibre?

Total Internal Reflection.


REAL-WORLD OPTICS

These principles are used in:

• Cameras
• Spectacles
• Microscopes
• Telescopes
• Fiber optics
• Medical equipment
• Optical sensors
• Robotics vision systems


ROBOTICS CONNECTION

Robot Camera:

Incoming light

→ Lens

→ Image sensor

→ Digital image

→ Computer vision

→ Object detection / navigation


FINAL CONNECTION

Surface
→ Reflection


New medium
→ Refraction


Material property
→ Refractive Index


Incident + Refraction angles
→ Snell's Law


High-to-low index at large angle
→ Total Internal Reflection


Controlled light
→ Imaging and sensing


KEY TAKEAWAY

Light can reflect,
refract and be guided.

Understanding how its speed
and direction change allows us
to design modern optical systems.
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
    print(" TOPIC 9 ENGLISH VIDEO UPDATED")
    print("==========================================")
    print("")

    print(f"Topic ID : {topic.id}")
    print(f"Topic    : {topic.title}")
    print(f"Video ID : {video.id}")
    print(f"Title    : {video.title}")
    print(f"URL      : {video.resource_url}")
    print(f"Active   : {video.is_active}")
    print("Language : English")
    print("")


except Exception as error:

    db.rollback()

    print("")
    print("TOPIC 9 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()