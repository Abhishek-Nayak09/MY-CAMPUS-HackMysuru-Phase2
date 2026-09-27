
(function () {

    "use strict";


    const API_BASE =
        "http://127.0.0.1:8000";


    function getTopicId() {

        const params =
            new URLSearchParams(
                window.location.search
            );


        const value =
            Number(
                params.get(
                    "topic_id"
                )
            );


        return (
            Number.isFinite(
                value
            )
            &&
            value > 0
        )
            ? value
            : null;
    }


    function getStudentId() {

        try {

            const raw =
                localStorage.getItem(
                    "myCampusUser"
                );


            if (!raw) {

                return null;
            }


            const user =
                JSON.parse(
                    raw
                );


            const value =
                Number(
                    user.id
                    ||
                    user.user_id
                    ||
                    user.userId
                    ||
                    0
                );


            return (
                Number.isFinite(
                    value
                )
                &&
                value > 0
            )
                ? value
                : null;


        } catch (error) {

            console.warn(
                "Could not read My Campus user",
                error
            );


            return null;
        }
    }


    async function saveEvent(
        eventName
    ) {

        const topicId =
            getTopicId();


        const studentId =
            getStudentId();


        if (
            !topicId
            ||
            !studentId
        ) {

            return null;
        }


        try {

            const response =
                await fetch(
                    `${API_BASE}/personalization/resource-event`,
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                student_id:
                                    studentId,

                                topic_id:
                                    topicId,

                                resource_type:
                                    "notes",

                                event:
                                    eventName
                            })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Personalization API returned ${response.status}`
                );
            }


            return await response.json();


        } catch (error) {

            console.warn(
                "Personalization event could not be saved",
                error
            );


            return null;
        }
    }


    function showToast(
        message
    ) {

        const oldToast =
            document.querySelector(
                ".resource-journey-toast"
            );


        if (oldToast) {

            oldToast.remove();
        }


        const toast =
            document.createElement(
                "div"
            );


        toast.className =
            "resource-journey-toast";


        toast.textContent =
            message;


        document.body.appendChild(
            toast
        );


        window.setTimeout(
            () => {

                toast.remove();

            },
            2600
        );
    }


    function buildBar() {

        if (
            document.querySelector(
                ".resource-journey-bar"
            )
        ) {

            return;
        }


        const topicId =
            getTopicId();


        if (!topicId) {

            return;
        }


        const bar =
            document.createElement(
                "div"
            );


        bar.className =
            "resource-journey-bar";


        const info =
            document.createElement(
                "div"
            );


        info.className =
            "resource-journey-info";


        const kicker =
            document.createElement(
                "div"
            );


        kicker.className =
            "resource-journey-kicker";


        kicker.textContent =
            `Topic ${topicId} • Current resource: Notes`;


        const title =
            document.createElement(
                "div"
            );


        title.className =
            "resource-journey-title";


        title.textContent =
            "Did Notes make the concept clear?";


        const subtitle =
            document.createElement(
                "div"
            );


        subtitle.className =
            "resource-journey-subtitle";


        subtitle.textContent =
            (
                "Continue only if you still need "
                +
                "another learning approach."
            );


        info.append(
            kicker,
            title,
            subtitle
        );


        const actions =
            document.createElement(
                "div"
            );


        actions.className =
            "resource-journey-actions";


        const nextButton =
            document.createElement(
                "button"
            );


        nextButton.type =
            "button";


        nextButton.className =
            (
                "resource-journey-btn "
                +
                "resource-journey-next"
            );


        nextButton.textContent =
            "Next → Video";


        const understoodButton =
            document.createElement(
                "button"
            );


        understoodButton.type =
            "button";


        understoodButton.className =
            (
                "resource-journey-btn "
                +
                "resource-journey-understood"
            );


        understoodButton.textContent =
            "✓ I Understood → Next Topic";


        nextButton.addEventListener(
            "click",
            async () => {

                nextButton.disabled =
                    true;


                understoodButton.disabled =
                    true;


                nextButton.textContent =
                    "Saving...";


                await saveEvent(
                    "next"
                );


                window.location.href =
                    `video.html?topic_id=${topicId}`;
            }
        );


        understoodButton.addEventListener(
            "click",
            async () => {

                nextButton.disabled =
                    true;


                understoodButton.disabled =
                    true;


                understoodButton.textContent =
                    "Saving learning preference...";


                const result =
                    await saveEvent(
                        "understood"
                    );


                if (
                    result
                    &&
                    result.preferred_resource_label
                ) {

                    showToast(
                        (
                            "Saved: you understood this topic through Notes. "
                            +
                            "Current preferred mode: "
                            +
                            result.preferred_resource_label
                            +
                            "."
                        )
                    );

                } else {

                    showToast(
                        (
                            "Saved: you understood "
                            +
                            "this topic through Notes."
                        )
                    );
                }


                const nextTopicId =
                    topicId + 1;


                window.setTimeout(
                    () => {

                        window.location.href =
                            (
                                "student.html"
                                +
                                `?next_topic_id=${nextTopicId}`
                                +
                                "&understood_via=notes"
                            );

                    },
                    650
                );
            }
        );


        actions.append(
            nextButton,
            understoodButton
        );


        bar.append(
            info,
            actions
        );


        document.body.appendChild(
            bar
        );
    }


    async function init() {

        const topicId =
            getTopicId();


        const studentId =
            getStudentId();


        if (
            !topicId
            ||
            !studentId
        ) {

            return;
        }


        buildBar();


        await saveEvent(
            "started"
        );
    }


    if (
        document.readyState
        ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            init
        );

    } else {

        init();
    }

})();
