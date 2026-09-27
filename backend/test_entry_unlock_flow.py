import json
from urllib.request import (
    Request,
    urlopen
)
from urllib.error import HTTPError


BASE_URL = "http://127.0.0.1:8000"

USER_ID = 1
SUBJECT_ID = 1
SOURCE_LEVEL_ID = 1


# ============================================================
# HTTP HELPERS
# ============================================================

def get_json(url):

    with urlopen(url) as response:

        return json.loads(
            response.read().decode("utf-8")
        )


def post_json(url, payload):

    body = json.dumps(
        payload
    ).encode("utf-8")


    request = Request(

        url,

        data=body,

        headers={
            "Content-Type": "application/json"
        },

        method="POST"
    )


    with urlopen(request) as response:

        return json.loads(
            response.read().decode("utf-8")
        )


# ============================================================
# MAIN TEST
# ============================================================

try:

    print("")
    print("==============================================")
    print(" ENTRY -> BASICS UNLOCK FLOW TEST")
    print("==============================================")
    print("")


    # --------------------------------------------------------
    # 1. CHECK INITIAL STATUS
    # --------------------------------------------------------

    status_before = get_json(

        f"{BASE_URL}"
        f"/level-tests/status/"
        f"{USER_ID}/"
        f"{SUBJECT_ID}"
    )


    print("1. CURRENT LEVEL STATUS")
    print("------------------------------")


    for level in status_before["levels"]:

        print(
            f"{level['level_name']:<15} "
            f"Unlocked: {level['is_unlocked']} "
            f"| Best Score: {level['best_score']}"
        )


    # --------------------------------------------------------
    # 2. FETCH REAL ENTRY TEST
    # --------------------------------------------------------

    test = get_json(

        f"{BASE_URL}"
        f"/level-tests/test/"
        f"{USER_ID}/"
        f"{SOURCE_LEVEL_ID}"
    )


    print("")
    print("2. TEST FETCHED")
    print("------------------------------")

    print(
        f"Source Level : "
        f"{test['source_level']['name']}"
    )

    print(
        f"Target Level : "
        f"{test['target_level']['name']}"
    )

    print(
        f"Questions    : "
        f"{test['total_questions']}"
    )

    print(
        f"Pass Rule    : "
        f"{test['pass_rule']}"
    )

    print("")


    for question in test["questions"]:

        print(
            f"Q{question['order']}: "
            f"{question['question']}"
        )


    # --------------------------------------------------------
    # 3. PREPARE EXACTLY 8 CORRECT + 2 WRONG
    # --------------------------------------------------------

    correct_answers = {

        1:
            "Matter, energy, motion and their interactions",

        2:
            "Braking a moving bicycle",

        3:
            "Force",

        4:
            "Electric motor",

        5:
            "It helps predict and understand how physical systems behave",

        6:
            "0 m",

        7:
            "50 km/h",

        8:
            "Velocity"
    }


    deliberate_wrong_answers = {

        9:
            "They have the same velocity",

        10:
            "Distance × Time"
    }


    answers = []


    for question in test["questions"]:

        order = question["order"]


        if order in correct_answers:

            selected_answer = (
                correct_answers[order]
            )


        elif order in deliberate_wrong_answers:

            selected_answer = (
                deliberate_wrong_answers[order]
            )


        else:

            raise Exception(
                f"Unexpected question order: {order}"
            )


        answers.append({

            "question_id":
                question["id"],

            "selected_answer":
                selected_answer
        })


    # --------------------------------------------------------
    # 4. SUBMIT TEST
    # --------------------------------------------------------

    result = post_json(

        f"{BASE_URL}"
        f"/level-tests/submit/"
        f"{SOURCE_LEVEL_ID}",

        {
            "user_id":
                USER_ID,

            "answers":
                answers
        }
    )


    print("")
    print("3. TEST RESULT")
    print("------------------------------")

    print(
        f"Score               : "
        f"{result['score']}/"
        f"{result['total_questions']}"
    )

    print(
        f"Required Score      : "
        f"{result['required_score']}/10"
    )

    print(
        f"Passed              : "
        f"{result['passed']}"
    )

    print(
        f"Target Unlocked     : "
        f"{result['target_level_unlocked']}"
    )

    print(
        f"Newly Unlocked      : "
        f"{result['newly_unlocked']}"
    )

    print(
        f"Wrong Answers       : "
        f"{result['wrong_count']}"
    )

    print("")

    print(
        result["message"]
    )


    # --------------------------------------------------------
    # 5. CONCEPT GAP FEEDBACK
    # --------------------------------------------------------

    print("")
    print("4. IDENTIFIED CONCEPT GAPS")
    print("------------------------------")


    if not result["wrong_answers"]:

        print(
            "No concept gaps detected."
        )


    else:

        for index, item in enumerate(
            result["wrong_answers"],
            start=1
        ):

            print("")
            print(
                f"GAP {index}"
            )

            print(
                f"Topic      : "
                f"{item['topic']['title']}"
            )

            print(
                f"Concept    : "
                f"{item['concept_gap']}"
            )

            print(
                f"Question   : "
                f"{item['question']}"
            )

            print(
                f"Selected   : "
                f"{item['selected_answer']}"
            )

            print(
                f"Correct    : "
                f"{item['correct_answer']}"
            )

            print(
                f"Explanation: "
                f"{item['explanation']}"
            )


    # --------------------------------------------------------
    # 6. CHECK LEVEL STATUS AGAIN
    # --------------------------------------------------------

    status_after = get_json(

        f"{BASE_URL}"
        f"/level-tests/status/"
        f"{USER_ID}/"
        f"{SUBJECT_ID}"
    )


    print("")
    print("5. LEVEL STATUS AFTER TEST")
    print("------------------------------")


    for level in status_after["levels"]:

        print(
            f"{level['level_name']:<15} "
            f"Unlocked: {level['is_unlocked']} "
            f"| Best Score: {level['best_score']}"
        )


    # --------------------------------------------------------
    # 7. FINAL AUTOMATED VALIDATION
    # --------------------------------------------------------

    basics = next(

        level

        for level in status_after["levels"]

        if level["level_name"].lower()
        == "basics"
    )


    print("")
    print("==============================================")


    if (
        result["score"] == 8
        and result["passed"] is True
        and basics["is_unlocked"] is True
        and result["wrong_count"] == 2
    ):

        print(
            "✅ ENTRY -> BASICS UNLOCK SYSTEM PASSED"
        )


    else:

        print(
            "❌ UNLOCK SYSTEM VALIDATION FAILED"
        )


    print("==============================================")
    print("")


except HTTPError as error:

    print("")
    print("HTTP ERROR")
    print(
        "Status:",
        error.code
    )

    print(
        error.read().decode(
            "utf-8"
        )
    )


except Exception as error:

    print("")
    print("TEST ERROR:")
    print(error)
    print("")