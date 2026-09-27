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
    # TOPIC 6
    # =========================================================

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


    # =========================================================
    # VIDEO DETAILS
    # =========================================================

    video_title = (
        "Sound Waves, Frequency, Wavelength & Wave Speed"
    )


    video_description = (
        "A guided Physics lesson covering sound waves, "
        "frequency, wavelength, wave speed, intensity "
        "and important sound-wave concepts."
    )


    youtube_url = (
        "https://www.youtube.com/watch?v=yVBtcAEHLfU"
    )


    learning_guide = """
BEFORE YOU WATCH

You already studied:

• Vibrations
• Waves
• Amplitude
• Frequency
• Wavelength
• Wave speed
• Sound
• Pitch
• Loudness
• Echo

through the Rich Notes.

Now use this video to strengthen
how these quantities are connected.


WHAT TO LOOK FOR

1. What creates a sound wave?

2. Why does sound need a medium?

3. What does frequency mean?

4. What is wavelength?

5. How are wave speed, frequency and wavelength related?

6. How does frequency affect pitch?

7. How does amplitude relate to loudness?

8. How can sound waves reflect?


VIBRATION

Sound begins with vibration.

Examples:

• Speaker cone vibrating
• Guitar string vibrating
• Vocal cords vibrating
• Drum surface vibrating


The vibrating object disturbs
the particles around it.


This disturbance travels outward
as a sound wave.


SOUND IS A MECHANICAL WAVE

Sound requires a material medium.

Examples:

• Air
• Water
• Solids


Sound cannot travel through
a perfect vacuum.


WHY?

Because there are no particles
available to transfer the vibration.


SOUND IN AIR

Air particles move back and forth.

This creates alternating regions of:


COMPRESSION

Particles are closer together.


RAREFACTION

Particles are farther apart.


These regions travel through the medium.


IMPORTANT

The air particles do not travel
from the source all the way to your ear.

They mainly vibrate around
their equilibrium positions.

The ENERGY travels through the medium.


FREQUENCY

Frequency tells us
how many complete vibrations occur per second.


Symbol:

f


Unit:

Hertz

Hz


Example:

100 Hz

means:

100 cycles every second.


PITCH CONNECTION

Higher Frequency
→ Higher Pitch


Lower Frequency
→ Lower Pitch


REAL-WORLD EXAMPLE

Bass note
→ Lower frequency


Sharp whistle
→ Higher frequency


AMPLITUDE

Amplitude describes
the maximum displacement from equilibrium.


For sound:

Greater amplitude generally corresponds
to greater sound intensity
and a louder perceived sound.


DO NOT CONFUSE

Frequency
→ Pitch


Amplitude
→ Loudness


WAVELENGTH

Wavelength is the distance between
corresponding points on consecutive waves.


Symbol:

λ


Examples:

Crest to crest

or

Compression to compression


WAVE SPEED

The important wave equation is:


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


IMPORTANT CONNECTION

If wave speed remains constant:

Higher frequency
→ Shorter wavelength


Lower frequency
→ Longer wavelength


TIME PERIOD

Time period is the time required
for one complete cycle.


Symbol:

T


Relationship:

f = 1 / T


and therefore:

T = 1 / f


REAL-WORLD EXAMPLE

If:

f = 10 Hz


Then:

T = 1 / 10

T = 0.1 s


SOUND INTENSITY

Sound intensity describes
how much sound power passes
through a certain area.


Greater sound intensity
generally corresponds to a louder sound.


Sound levels are commonly expressed
using decibels:

dB


REFLECTION OF SOUND

Sound waves can reflect
from surfaces.


When the reflected sound
returns after enough delay,
we hear an:

ECHO


REAL-WORLD CONNECTION

Echo and sound reflection are used in:

• Sonar
• Ultrasonic sensing
• Distance measurement
• Medical ultrasound concepts
• Acoustic testing


ECHO DISTANCE IDEA

Sound travels:

Source
→ Object
→ Source


So measured time includes
the complete round trip.


Distance to object:

Distance = v × t / 2


SELF CHECK 1

A source vibrates 200 times
every second.

Frequency:

200 Hz


SELF CHECK 2

Frequency = 10 Hz

Wavelength = 3 m


Wave speed:

v = fλ

v = 10 × 3

v = 30 m/s


SELF CHECK 3

Which property mainly affects pitch?

Frequency.


SELF CHECK 4

Why can sound not travel
through a perfect vacuum?

Because there are no particles
to transfer the vibration.


REAL-WORLD APPLICATIONS

Waves and sound are used in:

• Music
• Speakers
• Microphones
• Smartphones
• Ultrasound
• Sonar
• Robotics
• Ultrasonic sensors
• Acoustic engineering
• Noise control


ROBOTICS CONNECTION

An ultrasonic sensor:

1. Sends a sound pulse.

2. Pulse travels toward an object.

3. Sound reflects.

4. Sensor detects the echo.

5. Travel time is measured.

6. Distance is calculated.


AFTER WATCHING

You should be able to explain:


VIBRATION

Repeated back-and-forth motion.


WAVE

A disturbance that transfers energy.


FREQUENCY

Cycles per second.


WAVELENGTH

Spacing between repeated points of a wave.


WAVE SPEED

v = fλ


PITCH

Mainly related to frequency.


LOUDNESS

Closely related to amplitude.


ECHO

A reflected sound wave heard after a delay.


FINAL CONNECTION

Vibration
→ Creates wave


Wave
→ Transfers energy


Frequency
→ Determines pitch


Amplitude
→ Influences loudness


Frequency × Wavelength
→ Wave speed


Sound reflection
→ Echo


KEY TAKEAWAY

Sound starts with vibration.

The vibration produces a wave,
and that wave transfers energy
through a material medium.
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
    # CREATE
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


    # =========================================================
    # UPDATE
    # =========================================================

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
    print(" TOPIC 6 YOUTUBE VIDEO UPDATED")
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
    print("TOPIC 6 VIDEO UPDATE ERROR:")
    print(error)
    print("")


finally:

    db.close()