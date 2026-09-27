
(function () {

    "use strict";


    const API_BASE =
        "http://127.0.0.1:8000";


    /*
        Current real game availability.

        When Topic 2, 3... Unity/WebGL games are created,
        simply add those topic IDs here.
    */

    const GAME_TOPICS =
        new Set([
            1
        ]);


    const RESOURCE_LABELS = {

        notes:
            "Notes",

        video:
            "Video",

        interactive:
            "Interactive / Graphs",

        game:
            "Game",

        ai_tutor:
            "AI Tutor",

        faculty:
            "Faculty"
    };


    // ========================================================
    // BASIC HELPERS
    // ========================================================

    function getTopicId() {

        const params =
            new URLSearchParams(
                window.location.search
            );


        let topicId =
            Number(
                params.get(
                    "topic_id"
                )
            );


        if (
            Number.isFinite(topicId)
            &&
            topicId > 0
        ) {

            return topicId;
        }


        const path =
            window.location.pathname;


        const interactiveMatch =
            path.match(
                /interactive_topic_(\d+)\.html/i
            );


        if (interactiveMatch) {

            return Number(
                interactiveMatch[1]
            );
        }


        const gameMatch =
            path.match(
                /game_topic_(\d+)\.html/i
            );


        if (gameMatch) {

            return Number(
                gameMatch[1]
            );
        }


        if (
            path.endsWith(
                "/interactive.html"
            )
        ) {

            return 1;
        }


        return null;
    }


    function positiveNumber(
        value
    ) {

        const number =
            Number(
                value
            );


        if (
            Number.isFinite(number)
            &&
            number > 0
        ) {

            return number;
        }


        return null;
    }


    function userIdFromObject(
        object
    ) {

        if (
            !object
            ||
            typeof object !== "object"
        ) {

            return null;
        }


        const possibilities = [

            object.student_id,

            object.studentId,

            object.user_id,

            object.userId,

            object.id
        ];


        for (
            const candidate
            of possibilities
        ) {

            const value =
                positiveNumber(
                    candidate
                );


            if (value) {

                return value;
            }
        }


        return null;
    }


    function searchStorage(
        storage
    ) {

        const directKeys = [

            "student_id",

            "studentId",

            "user_id",

            "userId"
        ];


        for (
            const key
            of directKeys
        ) {

            const value =
                positiveNumber(
                    storage.getItem(
                        key
                    )
                );


            if (value) {

                return value;
            }
        }


        const jsonKeys = [

            "myCampusUser",

            "currentUser",

            "loggedInUser",

            "user",

            "student",

            "portalUser"
        ];


        for (
            const key
            of jsonKeys
        ) {

            const raw =
                storage.getItem(
                    key
                );


            if (!raw) {

                continue;
            }


            try {

                const object =
                    JSON.parse(
                        raw
                    );


                const value =
                    userIdFromObject(
                        object
                    );


                if (value) {

                    return value;
                }


            } catch (error) {

                // Ignore.
            }
        }


        return null;
    }


    function getStudentId() {

        try {

            if (
                typeof window.getUserId
                === "function"
            ) {

                const value =
                    positiveNumber(
                        window.getUserId()
                    );


                if (value) {

                    return value;
                }
            }


        } catch (error) {

            console.warn(
                error
            );
        }


        try {

            const value =
                searchStorage(
                    window.localStorage
                );


            if (value) {

                return value;
            }


        } catch (error) {

            console.warn(
                error
            );
        }


        try {

            const value =
                searchStorage(
                    window.sessionStorage
                );


            if (value) {

                return value;
            }


        } catch (error) {

            console.warn(
                error
            );
        }


        /*
            Hack Mysuru local development student.
        */

        if (
            window.location.hostname
            === "127.0.0.1"
            ||
            window.location.hostname
            === "localhost"
        ) {

            return 1;
        }


        return null;
    }


    // ========================================================
    // CURRENT RESOURCE
    // ========================================================

    function currentResource() {

        const filename =
            window.location.pathname
                .split("/")
                .pop()
                .toLowerCase();


        if (
            filename ===
            "notes.html"
        ) {

            return "notes";
        }


        if (
            filename ===
            "video.html"
        ) {

            return "video";
        }


        if (
            filename ===
            "interactive.html"
            ||
            filename.startsWith(
                "interactive_topic_"
            )
        ) {

            return "interactive";
        }


        if (
            filename.startsWith(
                "game_topic_"
            )
        ) {

            return "game";
        }


        if (
            filename ===
            "student.html"
        ) {

            return "student";
        }


        return null;
    }


    // ========================================================
    // PERSONALIZATION EVENT
    // ========================================================

    async function saveEvent(
        topicId,
        resource,
        eventName
    ) {

        const studentId =
            getStudentId();


        if (
            !studentId
            ||
            !topicId
            ||
            !resource
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
                                    resource,

                                event:
                                    eventName
                            }),

                        keepalive:
                            true
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `HTTP ${response.status}`
                );
            }


            return await response.json();


        } catch (error) {

            console.warn(
                "Learning journey event failed:",
                error
            );


            return null;
        }
    }


    // ========================================================
    // ROUTES
    // ========================================================

    function interactiveUrl(
        topicId
    ) {

        if (
            Number(topicId)
            === 1
        ) {

            return (
                `interactive.html?topic_id=${topicId}`
            );
        }


        return (
            `interactive_topic_${topicId}.html?topic_id=${topicId}`
        );
    }


    function aiTutorUrl(
        topicId
    ) {

        return (
            "student.html"
            +
            `?open_ai_topic=${topicId}`
        );
    }


    function facultyUrl(
        topicId
    ) {

        return (
            "student.html"
            +
            `?open_faculty_topic=${topicId}`
        );
    }


    function nextResourceInfo(
        resource,
        topicId
    ) {

        if (
            resource ===
            "notes"
        ) {

            return {
                resource:
                    "video",

                label:
                    "Video",

                url:
                    `video.html?topic_id=${topicId}`
            };
        }


        if (
            resource ===
            "video"
        ) {

            return {
                resource:
                    "interactive",

                label:
                    "Interactive / Graphs",

                url:
                    interactiveUrl(
                        topicId
                    )
            };
        }


        if (
            resource ===
            "interactive"
        ) {

            if (
                GAME_TOPICS.has(
                    Number(
                        topicId
                    )
                )
            ) {

                return {
                    resource:
                        "game",

                    label:
                        "Game",

                    url:
                        `game_topic_${topicId}.html?topic_id=${topicId}`
                };
            }


            return {
                resource:
                    "ai_tutor",

                label:
                    "AI Tutor",

                url:
                    aiTutorUrl(
                        topicId
                    ),

                note:
                    "Game for this topic is not built yet, so the next available learning mode is AI Tutor."
            };
        }


        if (
            resource ===
            "game"
        ) {

            return {
                resource:
                    "ai_tutor",

                label:
                    "AI Tutor",

                url:
                    aiTutorUrl(
                        topicId
                    )
            };
        }


        if (
            resource ===
            "ai_tutor"
        ) {

            return {
                resource:
                    "faculty",

                label:
                    "Faculty",

                url:
                    facultyUrl(
                        topicId
                    )
            };
        }


        return null;
    }


    // ========================================================
    // TOAST
    // ========================================================

    function showToast(
        message
    ) {

        const old =
            document.querySelector(
                ".journey-toast"
            );


        if (old) {

            old.remove();
        }


        const toast =
            document.createElement(
                "div"
            );


        toast.className =
            "journey-toast";


        toast.textContent =
            message;


        document.body.appendChild(
            toast
        );


        window.setTimeout(
            () => {

                toast.remove();

            },
            2300
        );
    }


    // ========================================================
    // NEXT TOPIC
    // ========================================================

    async function understoodAndNextTopic(
        topicId,
        resource,
        button
    ) {

        if (button) {

            button.disabled =
                true;


            button.textContent =
                "Saving...";
        }


        const result =
            await saveEvent(
                topicId,
                resource,
                "understood"
            );


        if (
            result
            &&
            result.preferred_resource_label
        ) {

            showToast(
                (
                    "Learning style updated: "
                    +
                    result.preferred_resource_label
                )
            );

        } else {

            showToast(
                (
                    "Saved: you understood through "
                    +
                    RESOURCE_LABELS[
                        resource
                    ]
                )
            );
        }


        if (
            Number(topicId)
            >= 10
        ) {

            window.setTimeout(
                () => {

                    window.location.href =
                        "student.html";

                },
                500
            );


            return;
        }


        const nextTopicId =
            Number(topicId)
            +
            1;


        window.setTimeout(
            () => {

                window.location.href =
                    (
                        "student.html"
                        +
                        `?next_topic_id=${nextTopicId}`
                        +
                        `&understood_via=${resource}`
                    );

            },
            500
        );
    }


    // ========================================================
    // NEXT RESOURCE
    // ========================================================

    async function continueToNextResource(
        topicId,
        resource,
        info,
        button
    ) {

        if (!info) {

            return;
        }


        if (button) {

            button.disabled =
                true;


            button.textContent =
                "Opening...";
        }


        await saveEvent(
            topicId,
            resource,
            "next"
        );


        window.location.href =
            info.url;
    }


    // ========================================================
    // STANDALONE RESOURCE BAR
    // Notes / Video / Interactive / Game
    // ========================================================

    function buildResourceBar(
        topicId,
        resource
    ) {

        if (
            document.getElementById(
                "universalJourneyBar"
            )
        ) {

            return;
        }


        const nextInfo =
            nextResourceInfo(
                resource,
                topicId
            );


        if (!nextInfo) {

            return;
        }


        document.body.classList.add(
            "journey-resource-page"
        );


        const bar =
            document.createElement(
                "div"
            );


        bar.id =
            "universalJourneyBar";


        bar.className =
            "my-campus-journey-bar";


        const left =
            document.createElement(
                "div"
            );


        left.className =
            "my-campus-journey-left";


        const stage =
            document.createElement(
                "div"
            );


        stage.className =
            "my-campus-journey-stage";


        stage.textContent =
            (
                `Topic ${topicId} • `
                +
                RESOURCE_LABELS[
                    resource
                ]
            );


        const question =
            document.createElement(
                "div"
            );


        question.className =
            "my-campus-journey-question";


        question.textContent =
            "Did this learning method make the topic clear?";


        const hint =
            document.createElement(
                "div"
            );


        hint.className =
            "my-campus-journey-hint";


        hint.textContent =
            nextInfo.note
            ||
            (
                "Understood? Stop here. "
                +
                "Still unclear? Continue to the next learning resource."
            );


        left.append(
            stage,
            question,
            hint
        );


        const actions =
            document.createElement(
                "div"
            );


        actions.className =
            "my-campus-journey-actions";


        const nextButton =
            document.createElement(
                "button"
            );


        nextButton.type =
            "button";


        nextButton.className =
            (
                "my-campus-journey-button "
                +
                "my-campus-journey-next"
            );


        nextButton.textContent =
            (
                `Next → ${nextInfo.label}`
            );


        const understoodButton =
            document.createElement(
                "button"
            );


        understoodButton.type =
            "button";


        understoodButton.className =
            (
                "my-campus-journey-button "
                +
                "my-campus-journey-understood"
            );


        understoodButton.textContent =
            "✓ I Understood → Next Topic";


        nextButton.addEventListener(
            "click",
            () => {

                continueToNextResource(
                    topicId,
                    resource,
                    nextInfo,
                    nextButton
                );
            }
        );


        understoodButton.addEventListener(
            "click",
            () => {

                understoodAndNextTopic(
                    topicId,
                    resource,
                    understoodButton
                );
            }
        );


        actions.append(
            nextButton,
            understoodButton
        );


        bar.append(
            left,
            actions
        );


        document.body.appendChild(
            bar
        );
    }


    // ========================================================
    // STUDENT TOPIC CARD HELPERS
    // ========================================================

    function findTopicCard(
        topicId
    ) {

        const indexes =
            document.querySelectorAll(
                ".topic-index"
            );


        for (
            const item
            of indexes
        ) {

            const content =
                (
                    item.textContent
                    ||
                    ""
                )
                    .trim()
                    .toUpperCase();


            if (
                content
                ===
                `TOPIC ${topicId}`
            ) {

                return item.closest(
                    ".topic-card"
                );
            }
        }


        return null;
    }


    function topicTitle(
        card,
        topicId
    ) {

        const title =
            card
            ?.querySelector(
                ".topic-title"
            );


        return (
            title
            ?.textContent
            ?.trim()
            ||
            `Topic ${topicId}`
        );
    }


    function waitForTopicCard(
        topicId
    ) {

        return new Promise(
            resolve => {

                const existing =
                    findTopicCard(
                        topicId
                    );


                if (existing) {

                    resolve(
                        existing
                    );

                    return;
                }


                const observer =
                    new MutationObserver(
                        () => {

                            const card =
                                findTopicCard(
                                    topicId
                                );


                            if (card) {

                                observer.disconnect();

                                resolve(
                                    card
                                );
                            }
                        }
                    );


                observer.observe(
                    document.body,
                    {
                        childList:
                            true,

                        subtree:
                            true
                    }
                );


                window.setTimeout(
                    () => {

                        observer.disconnect();

                        resolve(
                            findTopicCard(
                                topicId
                            )
                        );

                    },
                    12000
                );
            }
        );
    }


    // ========================================================
    // AI TUTOR JOURNEY CONTROLS
    // ========================================================

    function installAiTutorControls(
        topicId
    ) {

        const panel =
            document.getElementById(
                "embeddedAiTutorPanel"
            );


        if (!panel) {

            return;
        }


        if (
            panel.querySelector(
                ".ai-journey-actions"
            )
        ) {

            return;
        }


        const compose =
            panel.querySelector(
                ".embedded-ai-compose"
            );


        if (!compose) {

            return;
        }


        const holder =
            document.createElement(
                "div"
            );


        holder.className =
            "ai-journey-actions";


        const facultyButton =
            document.createElement(
                "button"
            );


        facultyButton.type =
            "button";


        facultyButton.className =
            (
                "ai-journey-action "
                +
                "ai-journey-next"
            );


        facultyButton.textContent =
            "Next → Faculty";


        const understoodButton =
            document.createElement(
                "button"
            );


        understoodButton.type =
            "button";


        understoodButton.className =
            (
                "ai-journey-action "
                +
                "ai-journey-understood"
            );


        understoodButton.textContent =
            "✓ I Understood → Next Topic";


        facultyButton.addEventListener(
            "click",
            async () => {

                await saveEvent(
                    topicId,
                    "ai_tutor",
                    "faculty_escalated"
                );


                if (
                    typeof window.closeEmbeddedAiTutor
                    === "function"
                ) {

                    window.closeEmbeddedAiTutor();
                }


                const card =
                    findTopicCard(
                        topicId
                    );


                const title =
                    topicTitle(
                        card,
                        topicId
                    );


                if (
                    typeof window.openFacultyModal
                    === "function"
                ) {

                    window.openFacultyModal({
                        id:
                            topicId,

                        title:
                            title
                    });

                } else {

                    window.location.href =
                        facultyUrl(
                            topicId
                        );
                }
            }
        );


        understoodButton.addEventListener(
            "click",
            () => {

                understoodAndNextTopic(
                    topicId,
                    "ai_tutor",
                    understoodButton
                );
            }
        );


        holder.append(
            facultyButton,
            understoodButton
        );


        compose.appendChild(
            holder
        );


        saveEvent(
            topicId,
            "ai_tutor",
            "started"
        );
    }


    // ========================================================
    // FACULTY MODAL CONTROLS
    // ========================================================

    function installFacultyControl(
        topicId
    ) {

        const modal =
            document.getElementById(
                "facultyModal"
            );


        if (!modal) {

            return;
        }


        const actions =
            modal.querySelector(
                ".modal-actions"
            );


        if (!actions) {

            return;
        }


        let button =
            actions.querySelector(
                ".faculty-journey-understood"
            );


        if (!button) {

            button =
                document.createElement(
                    "button"
                );


            button.type =
                "button";


            button.className =
                "faculty-journey-understood";


            button.textContent =
                "✓ Understood with Faculty → Next Topic";


            actions.appendChild(
                button
            );
        }


        button.onclick =
            () => {

                understoodAndNextTopic(
                    topicId,
                    "faculty",
                    button
                );
            };


        saveEvent(
            topicId,
            "faculty",
            "started"
        );
    }


    // ========================================================
    // OPEN AI/FACULTY FROM URL
    // ========================================================

    async function openRequestedStudentResource() {

        const params =
            new URLSearchParams(
                window.location.search
            );


        const aiTopic =
            positiveNumber(
                params.get(
                    "open_ai_topic"
                )
            );


        const facultyTopic =
            positiveNumber(
                params.get(
                    "open_faculty_topic"
                )
            );


        const requestedTopic =
            aiTopic
            ||
            facultyTopic;


        if (!requestedTopic) {

            return;
        }


        const card =
            await waitForTopicCard(
                requestedTopic
            );


        if (!card) {

            return;
        }


        const title =
            topicTitle(
                card,
                requestedTopic
            );


        if (aiTopic) {

            if (
                typeof window.openEmbeddedAiTutor
                === "function"
            ) {

                window.openEmbeddedAiTutor({
                    id:
                        aiTopic,

                    title:
                        title
                });


                window.setTimeout(
                    () => {

                        installAiTutorControls(
                            aiTopic
                        );

                    },
                    100
                );
            }
        }


        if (facultyTopic) {

            if (
                typeof window.openFacultyModal
                === "function"
            ) {

                window.openFacultyModal({
                    id:
                        facultyTopic,

                    title:
                        title
                });


                window.setTimeout(
                    () => {

                        installFacultyControl(
                            facultyTopic
                        );

                    },
                    100
                );
            }
        }


        const cleanUrl =
            new URL(
                window.location.href
            );


        cleanUrl.searchParams.delete(
            "open_ai_topic"
        );


        cleanUrl.searchParams.delete(
            "open_faculty_topic"
        );


        window.history.replaceState(
            {},
            "",
            cleanUrl.pathname
            +
            cleanUrl.search
        );
    }


    // ========================================================
    // WATCH AI / FACULTY WHEN OPENED DIRECTLY FROM TOPIC CARD
    // ========================================================

    function watchStudentDialogs() {

        const observer =
            new MutationObserver(
                () => {

                    const aiPanel =
                        document.getElementById(
                            "embeddedAiTutorPanel"
                        );


                    if (
                        aiPanel
                        &&
                        aiPanel.classList.contains(
                            "open"
                        )
                    ) {

                        const topicLine =
                            document.getElementById(
                                "embeddedAiTopicLine"
                            );


                        const match =
                            (
                                topicLine
                                ?.textContent
                                ||
                                ""
                            )
                                .match(
                                    /Topic\s+(\d+)/i
                                );


                        if (match) {

                            installAiTutorControls(
                                Number(
                                    match[1]
                                )
                            );
                        }
                    }


                    const facultyModal =
                        document.getElementById(
                            "facultyModal"
                        );


                    if (
                        facultyModal
                        &&
                        facultyModal.classList.contains(
                            "active"
                        )
                    ) {

                        const modalTopic =
                            document.getElementById(
                                "modalTopic"
                            )
                            ?.textContent
                            ?.trim();


                        const cards =
                            document.querySelectorAll(
                                ".topic-card"
                            );


                        for (
                            const card
                            of cards
                        ) {

                            const title =
                                card.querySelector(
                                    ".topic-title"
                                )
                                ?.textContent
                                ?.trim();


                            if (
                                title
                                &&
                                modalTopic
                                &&
                                title === modalTopic
                            ) {

                                const indexText =
                                    card.querySelector(
                                        ".topic-index"
                                    )
                                    ?.textContent
                                    ||
                                    "";


                                const match =
                                    indexText.match(
                                        /(\d+)/
                                    );


                                if (match) {

                                    installFacultyControl(
                                        Number(
                                            match[1]
                                        )
                                    );
                                }


                                break;
                            }
                        }
                    }
                }
            );


        observer.observe(
            document.body,
            {
                attributes:
                    true,

                childList:
                    true,

                subtree:
                    true,

                attributeFilter: [
                    "class"
                ]
            }
        );
    }


    // ========================================================
    // INIT
    // ========================================================

    async function init() {

        const resource =
            currentResource();


        if (!resource) {

            return;
        }


        if (
            resource ===
            "student"
        ) {

            watchStudentDialogs();

            await openRequestedStudentResource();

            return;
        }


        const topicId =
            getTopicId();


        if (!topicId) {

            console.warn(
                "Learning journey: topic_id missing."
            );

            return;
        }


        buildResourceBar(
            topicId,
            resource
        );


        await saveEvent(
            topicId,
            resource,
            "started"
        );
    }


    if (
        document.readyState
        === "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            init
        );

    } else {

        init();
    }

})();
