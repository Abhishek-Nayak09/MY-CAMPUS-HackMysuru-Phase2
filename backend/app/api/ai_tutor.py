import json
import os
import re
import urllib.error
import urllib.request

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.topic import Topic
from app.models.note import Note, NoteSection
from app.models.learning_content import LearningContent

# AI_TUTOR_VISUALS_V1
from app.services.ai_visuals import build_visuals_for_turn


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/ai-tutor",
    tags=["AI Tutor"]
)


# ============================================================
# PATHS
# ============================================================

THIS_FILE = Path(__file__).resolve()

BACKEND_DIR = THIS_FILE.parents[2]

PROJECT_ROOT = THIS_FILE.parents[3]


# ============================================================
# SIMPLE .ENV LOADER
# No extra python-dotenv dependency required
# ============================================================

def load_env_file(path: Path) -> None:

    if not path.exists():
        return

    try:

        lines = path.read_text(
            encoding="utf-8"
        ).splitlines()

    except Exception:
        return

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split(
            "=",
            1
        )

        key = key.strip()

        value = value.strip()

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in ("'", '"')
        ):
            value = value[1:-1]

        if key and key not in os.environ:

            os.environ[key] = value


load_env_file(
    PROJECT_ROOT / ".env"
)

load_env_file(
    BACKEND_DIR / ".env"
)


# ============================================================
# OPENAI CONFIG
# ============================================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
).strip()


OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-terra"
).strip()


OPENAI_RESPONSES_URL = (
    "https://api.openai.com/v1/responses"
)


# ============================================================
# REQUEST / RESPONSE SCHEMAS
# ============================================================

class HistoryMessage(BaseModel):

    role: str

    content: str


class TutorChatRequest(BaseModel):

    student_id: int | None = None

    topic_id: int

    topic_title: str | None = None

    message: str

    mode: str = "normal"

    history: list[HistoryMessage] = Field(
        default_factory=list
    )


class TutorChatResponse(BaseModel):

    answer: str

    topic_id: int

    topic_title: str

    strategy: str

    provider: str

    model: str | None = None

    resources_used: list[str] = Field(
        default_factory=list
    )

    visuals: list[dict[str, Any]] = Field(
        default_factory=list
    )


# ============================================================
# EXPLANATION STRATEGIES
# ============================================================

ALTERNATIVE_STRATEGIES = [

    "fresh everyday analogy",

    "completely different real-life situation",

    "visual mental picture",

    "cause-and-effect explanation",

    "compare-and-contrast explanation",

    "step-by-step reasoning",

    "simple story-based explanation",

    "application-first explanation"

]


# ============================================================
# FALLBACK EXAMPLES
#
# These make the project useful even before an API key
# is configured.
# ============================================================

TOPIC_EXAMPLES = {

    1: [
        (
            "Look around your room. A fan rotates because electrical "
            "energy becomes motion. A bulb produces light. Your phone "
            "uses electricity, waves and electronics. Physics is the "
            "set of ideas that helps us explain why these things work."
        ),

        (
            "Imagine travelling from home to college. The vehicle moves, "
            "brakes slow it, mirrors reflect light, sound reaches your "
            "ears and your phone communicates using electromagnetic "
            "waves. One normal journey already contains many parts of Physics."
        ),

        (
            "When you kick a football, force changes its motion. Gravity "
            "pulls it downward and friction eventually slows it. Physics "
            "helps describe every stage of that simple action."
        ),

        (
            "A hospital also uses Physics: X-rays create medical images, "
            "ultrasound uses sound waves and many instruments depend on "
            "electricity and sensors."
        )
    ],


    2: [
        (
            "Imagine riding a bicycle from your house to college. "
            "The path you travel gives distance, while the change from "
            "your starting position to your final position gives displacement."
        ),

        (
            "A speedometer tells how fast a vehicle moves. If we also say "
            "the vehicle is moving north, we have added direction, which "
            "is important when describing velocity."
        ),

        (
            "Think of a person walking around a circular ground and returning "
            "to the starting point. They travelled a distance, but their final "
            "displacement is zero."
        ),

        (
            "On a map, motion becomes easier to imagine as a moving dot. "
            "Its changing position tells us motion, and how quickly that "
            "position changes tells us speed or velocity."
        )
    ],


    3: [
        (
            "When a bus suddenly brakes, your body tends to continue "
            "forward. That tendency to keep the current state of motion "
            "is inertia."
        ),

        (
            "Kick an empty football and it accelerates easily. Push a much "
            "heavier object with the same effort and its acceleration is "
            "smaller. This connects force, mass and acceleration."
        ),

        (
            "Push a shopping trolley gently and it accelerates a little. "
            "Push harder and it accelerates more. Add heavy bags and the "
            "same push becomes less effective."
        ),

        (
            "While walking, your foot pushes the ground backward. The ground "
            "pushes you forward. Those opposite forces illustrate the "
            "action-reaction idea."
        ),

        (
            "A rocket pushes hot gases backward. The gases exert an opposite "
            "force on the rocket, pushing it forward."
        ),

        (
            "Imagine a hockey puck moving on almost frictionless ice. "
            "Without a large opposing force, it keeps moving instead of "
            "suddenly stopping by itself."
        )
    ],


    4: [
        (
            "When you lift a school bag from the floor onto a table, "
            "your force causes movement through a distance. That is a "
            "simple example of mechanical work."
        ),

        (
            "Two students climb the same staircase. If both have similar "
            "mass, they may perform similar work, but the student who reaches "
            "the top faster produces more power."
        ),

        (
            "At the top of a slide you have gravitational potential energy. "
            "As you slide downward, that energy changes mainly into kinetic energy."
        ),

        (
            "A moving bicycle has kinetic energy. Applying the brakes transforms "
            "part of that mechanical energy mainly into thermal energy."
        )
    ],


    5: [
        (
            "A slowly moving tennis ball is easy to stop. A fast cricket ball "
            "is harder to stop because its momentum is larger."
        ),

        (
            "A loaded shopping trolley moving at the same speed as an empty "
            "trolley has greater momentum because its mass is greater."
        ),

        (
            "When two toy cars collide, their velocities change, but the total "
            "momentum of the isolated system can remain conserved."
        ),

        (
            "Airbags increase the time over which a passenger's momentum "
            "changes, helping reduce the average force experienced."
        )
    ],


    6: [
        (
            "A guitar string vibrates. That vibration disturbs the surrounding "
            "air and the disturbance travels toward your ear as sound."
        ),

        (
            "Drop a stone into still water. Ripples move outward even though "
            "the water itself does not travel all the way outward with the wave."
        ),

        (
            "A loudspeaker moves back and forth, creating compressions and "
            "rarefactions in air. Those pressure variations reach your ear."
        ),

        (
            "Increasing the frequency of a sound generally makes its pitch "
            "higher, while changing amplitude strongly affects how loud it sounds."
        )
    ],


    7: [
        (
            "A torch works only when its switch completes the electrical path. "
            "Then current can flow through the bulb or LED."
        ),

        (
            "Think of voltage as the electrical push that helps charges move "
            "through a circuit, while resistance opposes that motion."
        ),

        (
            "Your phone charger provides electrical energy through a controlled "
            "voltage and current so the battery can store energy."
        ),

        (
            "When you add resistance to a circuit while keeping voltage fixed, "
            "the current becomes smaller according to Ohm's law."
        )
    ],


    8: [
        (
            "An electric motor sends current through coils. Magnetic effects "
            "produce forces that create rotation."
        ),

        (
            "A generator works in the opposite direction: mechanical motion "
            "and a changing magnetic environment are used to produce electricity."
        ),

        (
            "An electric doorbell uses an electromagnet. Current creates a "
            "magnetic field that pulls part of the mechanism."
        ),

        (
            "Move a magnet near a coil and the changing magnetic field can "
            "induce an electrical effect in the coil."
        )
    ],


    9: [
        (
            "Look into a mirror. Light from your face reaches the mirror and "
            "reflects toward your eyes, allowing you to see the image."
        ),

        (
            "A straw placed in water can appear bent because light changes "
            "direction when moving between water and air."
        ),

        (
            "A camera lens refracts incoming light so that a focused image "
            "can form on the camera sensor."
        ),

        (
            "A magnifying glass bends light using a curved lens, making an "
            "object appear larger when placed appropriately."
        )
    ],


    10: [
        (
            "Solar cells interact with light at a microscopic level and use "
            "photon energy to help generate electrical energy."
        ),

        (
            "LEDs produce light because of processes occurring inside "
            "semiconductor materials at very small scales."
        ),

        (
            "Medical nuclear imaging uses radiation associated with atomic "
            "nuclei to help doctors observe processes inside the body."
        ),

        (
            "Modern electronic devices depend on quantum behaviour inside "
            "semiconductors, even though we cannot directly see those microscopic effects."
        )
    ]

}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(
    value: Any
) -> str:

    if value is None:
        return ""

    text = str(value)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def limit_text(
    value: str,
    limit: int
) -> str:

    value = clean_text(
        value
    )

    if len(value) <= limit:
        return value

    return (
        value[:limit].rstrip()
        + "..."
    )


def looks_like_another_way_request(
    message: str
) -> bool:

    message_lower = message.lower()

    phrases = [

        "another way",

        "different way",

        "explain again",

        "still don't understand",

        "still dont understand",

        "not understand",

        "didn't understand",

        "didnt understand",

        "artha aglilla",

        "artha agilla",

        "artha agta illa",

        "bere tara",

        "bere way",

        "innond tara",

        "matte explain",

        "simple aagi bere",

        "gotaglilla",

        "gotagilla"
    ]

    return any(
        phrase in message_lower
        for phrase in phrases
    )


def looks_like_kannada_english(
    message: str
) -> bool:

    message_lower = message.lower()

    markers = [

        "nange",

        "artha",

        "agilla",

        "aglilla",

        "agta",

        "andre",

        "enu",

        "yaake",

        "yake",

        "heli",

        "helu",

        "maadu",

        "madu",

        "beku",

        "beda",

        "bere",

        "tara",

        "gotilla",

        "gotagilla"
    ]

    score = sum(
        1
        for marker in markers
        if marker in message_lower
    )

    return score >= 2


# ============================================================
# DATABASE CONTEXT
# ============================================================

def get_topic_context(
    db: Session,
    topic_id: int
) -> dict[str, Any]:

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )


    if not topic:

        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )


    note = (
        db.query(Note)
        .filter(
            Note.topic_id == topic_id,
            Note.is_active == True
        )
        .order_by(
            Note.version.desc()
        )
        .first()
    )


    sections = []

    if note:

        sections = (
            db.query(NoteSection)
            .filter(
                NoteSection.note_id == note.id,
                NoteSection.is_active == True
            )
            .order_by(
                NoteSection.section_order
            )
            .all()
        )


    learning_methods = (
        db.query(LearningContent)
        .filter(
            LearningContent.topic_id == topic_id,
            LearningContent.is_active == True
        )
        .order_by(
            LearningContent.content_order
        )
        .all()
    )


    note_parts = []


    if note:

        if note.title:

            note_parts.append(
                f"NOTE TITLE: {clean_text(note.title)}"
            )


        if note.subtitle:

            note_parts.append(
                f"NOTE SUBTITLE: {clean_text(note.subtitle)}"
            )


        if note.introduction:

            note_parts.append(
                "INTRODUCTION: "
                + limit_text(
                    note.introduction,
                    1800
                )
            )


    for section in sections:

        heading = clean_text(
            section.heading
        )

        body = limit_text(
            section.body or "",
            1700
        )


        section_text = (
            f"SECTION {section.section_order}"
        )


        if heading:

            section_text += (
                f" - {heading}"
            )


        if body:

            section_text += (
                f"\n{body}"
            )


        if section.caption:

            section_text += (
                "\nMEDIA CAPTION: "
                + limit_text(
                    section.caption,
                    400
                )
            )


        if section.interactive_data:

            try:

                parsed_interactive = json.loads(
                    section.interactive_data
                )

                section_text += (
                    "\nINTERACTIVE NOTE DATA: "
                    + limit_text(
                        json.dumps(
                            parsed_interactive,
                            ensure_ascii=False
                        ),
                        1000
                    )
                )

            except Exception:

                section_text += (
                    "\nINTERACTIVE NOTE DATA: "
                    + limit_text(
                        section.interactive_data,
                        1000
                    )
                )


        note_parts.append(
            section_text
        )


    resource_parts = []

    resource_types = []


    for method in learning_methods:

        resource_type = clean_text(
            method.resource_type
        ) or "resource"


        resource_types.append(
            resource_type
        )


        block = (
            f"RESOURCE TYPE: {resource_type}"
        )


        if method.title:

            block += (
                "\nTITLE: "
                + clean_text(
                    method.title
                )
            )


        if method.description:

            block += (
                "\nDESCRIPTION: "
                + limit_text(
                    method.description,
                    1200
                )
            )


        if method.content_text:

            block += (
                "\nCONTENT: "
                + limit_text(
                    method.content_text,
                    2200
                )
            )


        if method.resource_url:

            block += (
                "\nRESOURCE URL EXISTS: yes"
            )


        resource_parts.append(
            block
        )


    notes_context = "\n\n".join(
        note_parts
    )


    resources_context = "\n\n".join(
        resource_parts
    )


    notes_context = limit_text(
        notes_context,
        15000
    )


    resources_context = limit_text(
        resources_context,
        8000
    )


    return {

        "topic_id":
            topic.id,

        "topic_title":
            clean_text(
                topic.title
            ),

        "topic_description":
            clean_text(
                topic.description
            ),

        "notes_context":
            notes_context,

        "resources_context":
            resources_context,

        "resource_types":
            sorted(
                set(
                    resource_types
                )
            ),

        "note_sections":
            len(sections),

        "learning_methods":
            len(learning_methods)
    }


# ============================================================
# HISTORY
# ============================================================

def prepare_history(
    request: TutorChatRequest
) -> list[dict[str, str]]:

    result = []


    for item in request.history[-12:]:

        role = clean_text(
            item.role
        ).lower()


        if role not in {
            "user",
            "assistant"
        }:
            continue


        content = limit_text(
            item.content,
            2200
        )


        if not content:
            continue


        result.append(
            {
                "role":
                    role,

                "content":
                    content
            }
        )


    # Frontend currently sends current user message
    # in history as well as request.message.
    # Remove the duplicate.
    if result:

        last = result[-1]

        if (
            last["role"] == "user"
            and clean_text(
                last["content"]
            )
            == clean_text(
                request.message
            )
        ):

            result.pop()


    return result


# ============================================================
# STRATEGY
# ============================================================

def choose_strategy(
    request: TutorChatRequest,
    history: list[dict[str, str]]
) -> str:

    mode = clean_text(
        request.mode
    ).lower()


    assistant_turns = sum(
        1
        for item in history
        if item["role"] == "assistant"
    )


    another_way = (
        mode in {
            "again",
            "another",
            "different"
        }
        or looks_like_another_way_request(
            request.message
        )
    )


    if another_way:

        index = max(
            assistant_turns - 1,
            0
        ) % len(
            ALTERNATIVE_STRATEGIES
        )

        return ALTERNATIVE_STRATEGIES[
            index
        ]


    if mode == "example":

        return (
            "fresh real-life example"
        )


    if mode == "steps":

        return (
            "step-by-step reasoning"
        )


    if mode == "simple":

        return (
            "plain-language beginner explanation"
        )


    return (
        "direct adaptive explanation"
    )


# ============================================================
# HISTORY -> TEXT
# ============================================================

def history_as_text(
    history: list[dict[str, str]]
) -> str:

    if not history:

        return (
            "No previous conversation."
        )


    blocks = []


    for index, item in enumerate(
        history,
        start=1
    ):

        speaker = (
            "STUDENT"
            if item["role"] == "user"
            else "AI TUTOR"
        )


        blocks.append(
            f"{index}. {speaker}: "
            f"{item['content']}"
        )


    return "\n".join(
        blocks
    )


# ============================================================
# SYSTEM INSTRUCTIONS FOR REAL AI
# ============================================================

def build_instructions(
    strategy: str,
    student_message: str
) -> str:

    language_instruction = (
        "The student's latest message uses Kannada-English. "
        "Reply naturally in simple Kannada-English written in Latin script, "
        "while keeping important Physics terms in English."
        if looks_like_kannada_english(
            student_message
        )
        else
        "Reply in the same language and style as the student's latest message."
    )


    return f"""
You are My Campus AI Tutor.

You are NOT a generic chatbot.
You are the final learning-support layer after the student has already tried
Notes, Video, Interactive learning and Game-based learning for the current topic.

Your job is to identify what the student still does not understand and teach
that SAME topic in a clearer way.

CURRENT EXPLANATION STRATEGY:
{strategy}

LANGUAGE RULE:
{language_instruction}

STRICT TEACHING RULES:

1. Stay focused on the CURRENT TOPIC and the student's exact doubt.

2. Use the supplied My Campus topic resources as the primary learning context.

3. Never claim that a Video, Interactive experiment or Game contains something
   unless that information actually appears in the supplied resource context.

4. If the student asks "another way", "explain again", "I still don't understand",
   or similar:
   - read all previous AI Tutor replies,
   - DO NOT repeat the same example,
   - DO NOT repeat the same analogy,
   - DO NOT merely paraphrase the previous answer,
   - use the CURRENT EXPLANATION STRATEGY,
   - introduce a genuinely different mental model.

5. When confusion continues, progressively move from:
   abstract -> concrete -> visual -> causal -> step-by-step -> familiar analogy.

6. Answer the actual question first.
   Do not begin with filler like "Sure!" or "Of course!".

7. Keep normal explanations concise and understandable.
   Usually about 100-220 words is enough unless the student asks for detail.

8. Use formulas only when they genuinely help the current doubt.

9. If using a formula, explain what every symbol means.

10. Prefer familiar examples from daily life, vehicles, sports, home,
    classroom, mobile phones, machines and common technology.

11. Do not turn every response into a quiz.

12. A tiny understanding check is allowed only when it genuinely helps,
    and should normally be one short question at most.

13. Never shame the student for not understanding.

14. Do not say you remember something that is not present in conversation history.

15. Avoid repeating sentences from previous AI Tutor responses.

16. If the student's doubt is vague, make the most useful interpretation from
    the current topic instead of immediately asking a clarification question.

17. If the student asks something unrelated to the current topic, briefly say
    that this Tutor session is focused on the current topic and guide them back.

When the student requests a graph, diagram, plot, drawing or visual:
- never say that you cannot show one,
- the My Campus interface can attach a visual below your answer,
- briefly explain what the visual represents,
- do not invent measured experimental data; treat generated graph values as teaching illustrations unless the supplied context provides real values.

Your response should feel like a patient expert teacher, not like a textbook.
""".strip()


# ============================================================
# BUILD REAL AI INPUT
# ============================================================

def build_ai_input(
    request: TutorChatRequest,
    context: dict[str, Any],
    history: list[dict[str, str]],
    strategy: str
) -> str:

    return f"""
CURRENT MY CAMPUS TOPIC

Topic ID:
{context["topic_id"]}

Topic Title:
{context["topic_title"]}

Topic Description:
{context["topic_description"] or "No description available."}


============================================================
NOTES CONTEXT
============================================================

{context["notes_context"] or "No active Notes content available."}


============================================================
OTHER LEARNING RESOURCE CONTEXT
============================================================

{context["resources_context"] or "No additional backend learning-method content available."}


============================================================
PREVIOUS TUTOR CONVERSATION
============================================================

{history_as_text(history)}


============================================================
THIS TURN
============================================================

Selected explanation strategy:
{strategy}

Student message:
{clean_text(request.message)}

Respond directly to the student.
""".strip()


# ============================================================
# OPENAI RESPONSES API
# ============================================================

def extract_openai_text(
    data: dict[str, Any]
) -> str:

    direct = data.get(
        "output_text"
    )


    if isinstance(
        direct,
        str
    ) and direct.strip():

        return direct.strip()


    collected = []


    output_items = data.get(
        "output",
        []
    )


    if not isinstance(
        output_items,
        list
    ):

        return ""


    for item in output_items:

        if not isinstance(
            item,
            dict
        ):
            continue


        content_items = item.get(
            "content",
            []
        )


        if not isinstance(
            content_items,
            list
        ):
            continue


        for block in content_items:

            if not isinstance(
                block,
                dict
            ):
                continue


            block_type = block.get(
                "type"
            )


            if block_type not in {
                "output_text",
                "text"
            }:
                continue


            text_value = block.get(
                "text"
            )


            if isinstance(
                text_value,
                str
            ) and text_value.strip():

                collected.append(
                    text_value.strip()
                )


    return "\n".join(
        collected
    ).strip()


def call_openai(
    instructions: str,
    ai_input: str
) -> str | None:

    if not OPENAI_API_KEY:

        return None


    payload = {

        "model":
            OPENAI_MODEL,

        "instructions":
            instructions,

        "input":
            ai_input,

        "max_output_tokens":
            700
    }


    body = json.dumps(
        payload
    ).encode(
        "utf-8"
    )


    request = urllib.request.Request(

        OPENAI_RESPONSES_URL,

        data=body,

        headers={
            "Authorization":
                f"Bearer {OPENAI_API_KEY}",

            "Content-Type":
                "application/json"
        },

        method="POST"
    )


    try:

        with urllib.request.urlopen(
            request,
            timeout=45
        ) as response:

            raw = response.read().decode(
                "utf-8"
            )


        data = json.loads(
            raw
        )


        answer = extract_openai_text(
            data
        )


        if answer:

            return answer


        print(
            "[AI Tutor] OpenAI returned no text."
        )


    except urllib.error.HTTPError as error:

        try:

            error_body = (
                error.read()
                .decode(
                    "utf-8",
                    errors="replace"
                )
            )

        except Exception:

            error_body = (
                "Unable to read API error body."
            )


        print(
            f"[AI Tutor] OpenAI HTTP {error.code}: "
            f"{error_body[:1000]}"
        )


    except Exception as error:

        print(
            "[AI Tutor] OpenAI request failed:",
            str(error)
        )


    return None


# ============================================================
# ADAPTIVE LOCAL FALLBACK
# ============================================================

def get_first_useful_note(
    context: dict[str, Any]
) -> str:

    notes = clean_text(
        context.get(
            "notes_context",
            ""
        )
    )


    if notes:

        return limit_text(
            notes,
            500
        )


    description = clean_text(
        context.get(
            "topic_description",
            ""
        )
    )


    return description


def local_fallback_answer(
    request: TutorChatRequest,
    context: dict[str, Any],
    history: list[dict[str, str]],
    strategy: str
) -> str:

    topic_id = int(
        context["topic_id"]
    )


    topic_title = (
        context["topic_title"]
    )


    examples = TOPIC_EXAMPLES.get(
        topic_id,
        []
    )


    assistant_turns = sum(
        1
        for item in history
        if item["role"] == "assistant"
    )


    if examples:

        example_index = (
            assistant_turns
            % len(examples)
        )

        example = examples[
            example_index
        ]

    else:

        example = (
            get_first_useful_note(
                context
            )
            or
            (
                f"{topic_title} can be understood by first "
                "identifying what is changing and why."
            )
        )


    core = (
        context["topic_description"]
        or get_first_useful_note(
            context
        )
        or topic_title
    )


    core = limit_text(
        core,
        420
    )


    kanglish = looks_like_kannada_english(
        request.message
    )


    if strategy == "fresh everyday analogy":

        if kanglish:

            return (
                f"Okay, bere tara imagine maadu.\n\n"
                f"{example}\n\n"
                f"Idu {topic_title} concept-na daily-life situation alli "
                f"noduva ondu way. Previous explanation-na memorize madodu beda; "
                f"illi yavudu change aagta ide mattu yaake change aagta ide "
                f"annodanna observe maadu."
            )

        return (
            f"Try a completely different picture:\n\n"
            f"{example}\n\n"
            f"This is another way to see {topic_title}: focus on what changes "
            f"and what causes that change instead of memorizing the definition."
        )


    if strategy == "completely different real-life situation":

        if kanglish:

            return (
                f"Innond real-life situation togolona:\n\n"
                f"{example}\n\n"
                f"Ee example alli concept-na definition inda start madilla. "
                f"First actual event nodi, admele adakke Physics rule connect "
                f"madta idivi. Ee approach usually concept easy-aagi click aagutte."
            )

        return (
            f"Let's switch to a different real-life situation:\n\n"
            f"{example}\n\n"
            f"Instead of starting from the definition, observe the event first "
            f"and then connect the Physics idea to what you saw."
        )


    if strategy == "visual mental picture":

        if kanglish:

            return (
                f"Mind alli scene imagine maadu:\n\n"
                f"{example}\n\n"
                f"Scene-na slow motion alli imagine maadi. First en situation ide, "
                f"next en change aaytu, matte aa change-ge reason enu anta nodu. "
                f"Ade {topic_title} artha madkoloke visual way."
            )

        return (
            f"Build a picture in your mind:\n\n"
            f"{example}\n\n"
            f"Now imagine the event in slow motion. Notice the starting situation, "
            f"what changes next, and what causes the change. That visual chain is "
            f"the key to understanding {topic_title}."
        )


    if strategy == "cause-and-effect explanation":

        if kanglish:

            return (
                f"{topic_title} na cause → effect tara nodona:\n\n"
                f"1. Ond situation ide.\n"
                f"2. Ond cause/action happen aagutte.\n"
                f"3. Adarinda observable change/effect barutte.\n\n"
                f"Example: {example}\n\n"
                f"Concept artha madkoloke 'yaake ee effect bantu?' anta kelodu "
                f"definition remember madodkinta useful."
            )

        return (
            f"Think in a cause → effect chain:\n\n"
            f"1. Start with the initial situation.\n"
            f"2. Identify the action or cause.\n"
            f"3. Observe the resulting change.\n\n"
            f"Example: {example}\n\n"
            f"The important question is: why did that effect happen?"
        )


    if strategy == "compare-and-contrast explanation":

        if kanglish:

            return (
                f"Compare maadi artha madkolona.\n\n"
                f"Situation A: action/change tumba kadime.\n"
                f"Situation B: ade type situation, but condition change aagide.\n\n"
                f"{example}\n\n"
                f"Eradu situations compare madidaga yav factor result-na change "
                f"madtu anta easy-aagi gothagutte. Adu {topic_title} na main idea-ge "
                f"connect aagutte."
            )

        return (
            f"Let's understand it by comparison.\n\n"
            f"Imagine two similar situations where only one important condition "
            f"changes.\n\n{example}\n\n"
            f"Comparing the outcomes shows which factor controls the behaviour. "
            f"That difference points to the central idea in {topic_title}."
        )


    if strategy == "step-by-step reasoning":

        if kanglish:

            return (
                f"{topic_title} step-by-step:\n\n"
                f"1. First situation yenu anta identify maadu.\n"
                f"2. Yav action/force/change ide anta nodu.\n"
                f"3. Adarinda en result bantu anta observe maadu.\n"
                f"4. Aa result-ge Physics concept connect maadu.\n\n"
                f"Example: {example}"
            )

        return (
            f"{topic_title}, step by step:\n\n"
            f"1. Identify the starting situation.\n"
            f"2. Identify the action or physical change.\n"
            f"3. Observe the result.\n"
            f"4. Connect that result to the Physics concept.\n\n"
            f"Example: {example}"
        )


    if strategy == "simple story-based explanation":

        if kanglish:

            return (
                f"Ond small story tara nodona:\n\n"
                f"{example}\n\n"
                f"Story alli event first nodu; technical word later connect maadu. "
                f"Ee tara concept memory-ge definition tara alla, actual experience "
                f"tara store aagutte."
            )

        return (
            f"Think of it as a short story:\n\n"
            f"{example}\n\n"
            f"Notice the event first and attach the technical Physics term only "
            f"after the behaviour makes sense."
        )


    if strategy == "application-first explanation":

        if kanglish:

            return (
                f"Definition side-ge swalpa bidi. First application nodona:\n\n"
                f"{example}\n\n"
                f"Ee application yaake work aagutte anta artha aadmele "
                f"{topic_title} definition naturally connect aagutte."
            )

        return (
            f"Forget the formal definition for a moment and start from an application:\n\n"
            f"{example}\n\n"
            f"Once you understand why the application behaves that way, the formal "
            f"idea of {topic_title} becomes much easier to connect."
        )


    if strategy == "fresh real-life example":

        return example


    if strategy == "step-by-step reasoning":

        return (
            f"{topic_title} can be broken into a simple chain:\n\n"
            f"Start condition → physical action → observable change → Physics rule.\n\n"
            f"{example}"
        )


    if kanglish:

        return (
            f"{topic_title} na simple aagi nodona.\n\n"
            f"{core}\n\n"
            f"Real-life connection:\n{example}"
        )


    return (
        f"{core}\n\n"
        f"A useful real-life way to see it is:\n{example}"
    )


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def ai_tutor_status():

    using_openai = bool(
        OPENAI_API_KEY
    )


    return {

        "status":
            "ready",

        "provider":
            (
                "openai"
                if using_openai
                else "adaptive_local_fallback"
            ),

        "model":
            (
                OPENAI_MODEL
                if using_openai
                else None
            ),

        "api_key_configured":
            using_openai,

        "message":
            (
                "Real AI provider is active."
                if using_openai
                else
                (
                    "Adaptive fallback is active. "
                    "Configure OPENAI_API_KEY for full LLM tutoring."
                )
            )
    }


# ============================================================
# CHAT
# ============================================================

@router.post(
    "/chat",
    response_model=TutorChatResponse
)
def ai_tutor_chat(
    request: TutorChatRequest,
    db: Session = Depends(get_db)
):

    student_message = clean_text(
        request.message
    )


    if not student_message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )


    if len(student_message) > 5000:

        raise HTTPException(
            status_code=400,
            detail="Message is too long"
        )


    context = get_topic_context(
        db,
        request.topic_id
    )


    history = prepare_history(
        request
    )


    strategy = choose_strategy(
        request,
        history
    )


    instructions = build_instructions(
        strategy,
        student_message
    )


    ai_input = build_ai_input(
        request,
        context,
        history,
        strategy
    )


    answer = call_openai(
        instructions,
        ai_input
    )


    if answer:

        provider = "openai"

        model = OPENAI_MODEL

    else:

        provider = (
            "adaptive_local_fallback"
        )

        model = None

        answer = local_fallback_answer(
            request,
            context,
            history,
            strategy
        )


    resources_used = [
        "topic"
    ]


    if context["note_sections"] > 0:

        resources_used.append(
            "notes"
        )


    resources_used.extend(
        context["resource_types"]
    )


    resources_used = sorted(
        set(
            resources_used
        )
    )


    visuals = build_visuals_for_turn(
        topic_id=context["topic_id"],
        topic_title=context["topic_title"],
        message=student_message,
        mode=request.mode,
        history=history,
    )


    return TutorChatResponse(

        answer=answer,

        topic_id=context[
            "topic_id"
        ],

        topic_title=context[
            "topic_title"
        ],

        strategy=strategy,

        provider=provider,

        model=model,

        resources_used=resources_used,

        visuals=visuals
    )