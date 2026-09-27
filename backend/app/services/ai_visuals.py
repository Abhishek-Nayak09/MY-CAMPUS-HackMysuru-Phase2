
from __future__ import annotations

import math
from typing import Any


VISUAL_WORDS = (
    "graph",
    "graphs",
    "chart",
    "plot",
    "diagram",
    "visual",
    "visualize",
    "visualise",
    "draw",
    "curve",
    "ray diagram",
    "figure",
    "image",
)


def _clean(
    value: Any
) -> str:

    return (
        " ".join(
            str(
                value
                or ""
            ).split()
        )
        .strip()
    )


def _wants_visual(
    message: str
) -> bool:

    text = (
        _clean(
            message
        )
        .lower()
    )

    return any(
        word in text
        for word in VISUAL_WORDS
    )


def _prior_visual_requests(
    history: list[
        dict[
            str,
            str
        ]
    ]
) -> int:

    total = 0

    for item in history:

        if (
            str(
                item.get(
                    "role",
                    ""
                )
            ).lower()
            != "user"
        ):
            continue

        if _wants_visual(
            str(
                item.get(
                    "content",
                    ""
                )
            )
        ):
            total += 1

    return total


def _line_chart(
    title: str,
    x_label: str,
    y_label: str,
    points: list[
        tuple[
            float,
            float
        ]
    ],
    caption: str,
) -> dict[
    str,
    Any
]:

    return {

        "kind":
            "line_chart",

        "title":
            title,

        "x_label":
            x_label,

        "y_label":
            y_label,

        "points": [

            {
                "x":
                    float(x),

                "y":
                    float(y)
            }

            for x, y
            in points
        ],

        "caption":
            caption
    }


def _diagram(
    diagram_type: str,
    title: str,
    caption: str,
) -> dict[
    str,
    Any
]:

    return {

        "kind":
            "diagram",

        "diagram":
            diagram_type,

        "title":
            title,

        "caption":
            caption
    }


# ============================================================
# TOPIC VISUAL LIBRARY
# ============================================================

def _topic_candidates(
    topic_id: int
) -> list[
    dict[
        str,
        Any
    ]
]:

    # --------------------------------------------------------
    # TOPIC 1
    # --------------------------------------------------------

    if topic_id == 1:

        return [

            _diagram(
                "physics_everyday",
                "Physics in everyday life",
                (
                    "A concept map connecting everyday "
                    "actions to motion, energy, light, "
                    "sound and electricity."
                ),
            ),

            _diagram(
                "energy_flow",
                "Everyday energy transformations",
                (
                    "A visual flow showing how one form "
                    "of energy can change into another "
                    "in common devices."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 2
    # --------------------------------------------------------

    if topic_id == 2:

        return [

            _line_chart(
                "Distance-time graph",
                "Time (s)",
                "Distance (m)",

                [
                    (0, 0),
                    (1, 2),
                    (2, 4),
                    (3, 6),
                    (4, 8),
                    (5, 10)
                ],

                (
                    "Illustrative constant-speed motion: "
                    "equal distance is covered in equal "
                    "time intervals."
                ),
            ),

            _line_chart(
                "Velocity-time graph",
                "Time (s)",
                "Velocity (m/s)",

                [
                    (0, 0),
                    (1, 2),
                    (2, 4),
                    (3, 4),
                    (4, 3),
                    (5, 1)
                ],

                (
                    "Illustrative motion showing "
                    "acceleration, constant velocity "
                    "and deceleration."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 3
    # --------------------------------------------------------

    if topic_id == 3:

        return [

            _line_chart(
                "Force vs acceleration",
                "Acceleration (m/s²)",
                "Force (N)",

                [
                    (0, 0),
                    (1, 2),
                    (2, 4),
                    (3, 6),
                    (4, 8),
                    (5, 10)
                ],

                (
                    "Illustrative F = ma relationship "
                    "for a constant mass of 2 kg."
                ),
            ),

            _diagram(
                "newton_forces",
                "Forces on a block",
                (
                    "A free-body style visual showing "
                    "applied force, friction, weight "
                    "and normal force."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 4
    # --------------------------------------------------------

    if topic_id == 4:

        return [

            _line_chart(
                "Work vs distance",
                "Distance (m)",
                "Work (J)",

                [
                    (0, 0),
                    (1, 10),
                    (2, 20),
                    (3, 30),
                    (4, 40),
                    (5, 50)
                ],

                (
                    "Illustrative W = Fd relationship "
                    "for a constant 10 N force acting "
                    "along the motion."
                ),
            ),

            _diagram(
                "energy_flow",
                "Energy transformation",
                (
                    "A simple visual showing energy "
                    "changing between stored, motion "
                    "and thermal forms."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 5
    # --------------------------------------------------------

    if topic_id == 5:

        return [

            _line_chart(
                "Momentum vs velocity",
                "Velocity (m/s)",
                "Momentum (kg·m/s)",

                [
                    (0, 0),
                    (1, 2),
                    (2, 4),
                    (3, 6),
                    (4, 8),
                    (5, 10)
                ],

                (
                    "Illustrative p = mv relationship "
                    "for a constant mass of 2 kg."
                ),
            ),

            _diagram(
                "collision",
                "Momentum during a collision",
                (
                    "A before-and-after visual for "
                    "two objects exchanging momentum."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 6
    # --------------------------------------------------------

    if topic_id == 6:

        wave_points = [

            (
                x / 4,

                math.sin(
                    (x / 4)
                    * math.pi
                )
            )

            for x
            in range(
                0,
                17
            )
        ]

        return [

            _line_chart(
                "Wave shape",
                "Position",
                "Displacement",
                wave_points,
                (
                    "Illustrative transverse wave "
                    "showing repeating crests "
                    "and troughs."
                ),
            ),

            _diagram(
                "longitudinal_wave",
                "Sound as a longitudinal wave",
                (
                    "A visual showing compressions "
                    "and rarefactions moving through "
                    "a medium."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 7
    # --------------------------------------------------------

    if topic_id == 7:

        return [

            _line_chart(
                "Voltage-current graph",
                "Current (A)",
                "Voltage (V)",

                [
                    (0, 0),
                    (0.5, 5),
                    (1, 10),
                    (1.5, 15),
                    (2, 20)
                ],

                (
                    "Illustrative Ohm's-law graph "
                    "for a 10 Ω resistor."
                ),
            ),

            _diagram(
                "simple_circuit",
                "Simple electric circuit",
                (
                    "A visual showing a battery, "
                    "switch, resistor/lamp and a "
                    "closed current path."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 8
    # --------------------------------------------------------

    if topic_id == 8:

        return [

            _diagram(
                "magnetic_field",
                (
                    "Magnetic field around a "
                    "current-carrying wire"
                ),
                (
                    "Concentric field lines show "
                    "the magnetic field surrounding "
                    "a straight current-carrying conductor."
                ),
            ),

            _line_chart(
                (
                    "Current vs magnetic-field "
                    "strength"
                ),
                "Current (A)",
                "Relative magnetic field",

                [
                    (0, 0),
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5)
                ],

                (
                    "Illustrative proportional trend "
                    "when geometry and observation "
                    "distance are fixed."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 9
    # --------------------------------------------------------

    if topic_id == 9:

        return [

            _diagram(
                "reflection",
                "Reflection ray diagram",
                (
                    "The angle of incidence equals "
                    "the angle of reflection, measured "
                    "from the normal."
                ),
            ),

            _diagram(
                "refraction",
                "Refraction ray diagram",
                (
                    "A light ray changes direction "
                    "when it enters a medium with a "
                    "different refractive index."
                ),
            ),

            _diagram(
                "convex_lens",
                "Convex lens ray diagram",
                (
                    "Parallel and central rays help "
                    "show how a convex lens can form "
                    "an image."
                ),
            ),
        ]


    # --------------------------------------------------------
    # TOPIC 10
    # --------------------------------------------------------

    if topic_id == 10:

        return [

            _line_chart(
                (
                    "Photon energy "
                    "vs frequency"
                ),
                "Relative frequency",
                "Relative photon energy",

                [
                    (0, 0),
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5)
                ],

                (
                    "Illustrative proportional "
                    "relationship from E = hf."
                ),
            ),

            _diagram(
                "energy_levels",
                "Atomic energy levels",
                (
                    "A simplified energy-level "
                    "visual showing absorption "
                    "and emission transitions."
                ),
            ),
        ]


    return []


# ============================================================
# CHOOSE BEST VISUAL
# ============================================================

def _keyword_pick(
    topic_id: int,
    message: str
) -> int | None:

    text = (
        _clean(
            message
        )
        .lower()
    )


    if topic_id == 2:

        if "velocity" in text:
            return 1

        if (
            "distance" in text
            or
            "motion" in text
        ):
            return 0


    if topic_id == 3:

        if (
            "force" in text
            and
            (
                "graph" in text
                or
                "acceleration" in text
            )
        ):
            return 0

        if (
            "free body" in text
            or
            "forces" in text
            or
            "diagram" in text
        ):
            return 1


    if topic_id == 4:

        if (
            "work" in text
            or
            "graph" in text
        ):
            return 0

        if "energy" in text:
            return 1


    if topic_id == 5:

        if (
            "momentum" in text
            and
            "graph" in text
        ):
            return 0

        if "collision" in text:
            return 1


    if topic_id == 6:

        if (
            "sound" in text
            or
            "longitudinal" in text
        ):
            return 1

        if (
            "wave" in text
            or
            "graph" in text
        ):
            return 0


    if topic_id == 7:

        if (
            "circuit" in text
            or
            "diagram" in text
        ):
            return 1

        if (
            "ohm" in text
            or
            "voltage" in text
            or
            "current" in text
            or
            "graph" in text
        ):
            return 0


    if topic_id == 8:

        if (
            "field" in text
            or
            "wire" in text
            or
            "diagram" in text
        ):
            return 0

        if (
            "graph" in text
            or
            "current" in text
        ):
            return 1


    if topic_id == 9:

        if (
            "reflection" in text
            or
            "mirror" in text
        ):
            return 0

        if (
            "refraction" in text
            or
            "water" in text
            or
            "straw" in text
        ):
            return 1

        if (
            "lens" in text
            or
            "camera" in text
            or
            "convex" in text
        ):
            return 2


    if topic_id == 10:

        if (
            "photon" in text
            or
            "frequency" in text
            or
            "graph" in text
        ):
            return 0

        if (
            "atom" in text
            or
            "energy level" in text
            or
            "transition" in text
        ):
            return 1


    return None


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def build_visuals_for_turn(
    topic_id: int,
    topic_title: str,
    message: str,
    mode: str,
    history: list[
        dict[
            str,
            str
        ]
    ],
) -> list[
    dict[
        str,
        Any
    ]
]:

    del topic_title
    del mode


    # Only attach when student explicitly asks
    # for visual / graph / diagram.

    if not _wants_visual(
        message
    ):

        return []


    candidates = (
        _topic_candidates(
            int(
                topic_id
            )
        )
    )


    if not candidates:

        return []


    direct_index = (
        _keyword_pick(
            int(
                topic_id
            ),
            message
        )
    )


    if (
        direct_index
        is not None
        and
        0
        <= direct_index
        < len(
            candidates
        )
    ):

        selected_index = (
            direct_index
        )

    else:

        selected_index = (
            _prior_visual_requests(
                history
            )
            %
            len(
                candidates
            )
        )


    selected = dict(
        candidates[
            selected_index
        ]
    )


    selected[
        "visual_id"
    ] = (
        f"topic-{topic_id}"
        f"-visual-"
        f"{selected_index + 1}"
    )


    selected[
        "educational"
    ] = True


    return [
        selected
    ]
