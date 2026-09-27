
(function () {

    "use strict";

    const API_BASE = "http://127.0.0.1:8000";


    // ========================================================
    // TOPIC ID
    // ========================================================

    function getTopicId() {

        const params = new URLSearchParams(
            window.location.search
        );

        const topicId = Number(
            params.get("topic_id")
        );

        if (
            Number.isFinite(topicId)
            &&
            topicId > 0
        ) {
            return topicId;
        }

        return null;
    }


    // ========================================================
    // STUDENT ID
    // Robust lookup for current My Campus login/session
    // ========================================================

    function readNumber(value) {

        const number = Number(value);

        if (
            Number.isFinite(number)
            &&
            number > 0
        ) {
            return number;
        }

        return null;
    }


    function idFromObject(object) {

        if (
            !object
            ||
            typeof object !== "object"
        ) {
            return null;
        }

        const candidates = [
            object.student_id,
            object.studentId,
            object.user_id,
            object.userId,
            object.id
        ];

        for (const candidate of candidates) {

            const value = readNumber(candidate);

            if (value) {
                return value;
            }
        }

        return null;
    }


    function inspectStorage(storage) {

        const directKeys = [
            "student_id",
            "studentId",
            "user_id",
            "userId"
        ];

        for (const key of directKeys) {

            const value = readNumber(
                storage.getItem(key)
            );

            if (value) {
                return value;
            }
        }


        const objectKeys = [
            "myCampusUser",
            "currentUser",
            "loggedInUser",
            "user",
            "authUser",
            "student",
            "portalUser"
        ];

        for (const key of objectKeys) {

            const raw = storage.getItem(key);

            if (!raw) {
                continue;
            }

            try {

                const parsed = JSON.parse(raw);

                const value = idFromObject(parsed);

                if (value) {
                    return value;
                }

            } catch (error) {
                // Ignore non-JSON values.
            }
        }


        // Last safe scan: inspect JSON objects stored by this local app.

        for (
            let index = 0;
            index < storage.length;
            index += 1
        ) {

            const key = storage.key(index);

            if (!key) {
                continue;
            }

            const raw = storage.getItem(key);

            if (!raw) {
                continue;
            }

            try {

                const parsed = JSON.parse(raw);

                const value = idFromObject(parsed);

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

        const params = new URLSearchParams(
            window.location.search
        );

        const urlStudentId = readNumber(
            params.get("student_id")
        );

        if (urlStudentId) {
            return urlStudentId;
        }


        try {

            if (
                typeof window.getUserId === "function"
            ) {

                const existingId = readNumber(
                    window.getUserId()
                );

                if (existingId) {
                    return existingId;
                }
            }

        } catch (error) {
            console.warn(error);
        }


        try {

            const sessionId = inspectStorage(
                window.sessionStorage
            );

            if (sessionId) {
                return sessionId;
            }

        } catch (error) {
            console.warn(error);
        }


        try {

            const localId = inspectStorage(
                window.localStorage
            );

            if (localId) {
                return localId;
            }

        } catch (error) {
            console.warn(error);
        }


        /*
            Local Hack Mysuru development fallback.

            Current project demo student = 1.
            This fallback is used only on localhost.
        */

        if (
            window.location.hostname === "127.0.0.1"
            ||
            window.location.hostname === "localhost"
        ) {
            return 1;
        }

        return null;
    }


    // ========================================================
    // PERSONALIZATION EVENT
    // ========================================================

    async function saveEvent(eventName) {

        const studentId = getStudentId();
        const topicId = getTopicId();

        if (
            !studentId
            ||
            !topicId
        ) {

            console.warn(
                "Personalization skipped: missing student/topic ID."
            );

            return null;
        }


        try {

            const response = await fetch(
                `${API_BASE}/personalization/resource-event`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        student_id: studentId,
                        topic_id: topicId,
                        resource_type: "notes",
                        event: eventName
                    }),

                    keepalive: true
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
                "Could not save learning event:",
                error
            );

            return null;
        }
    }


    // ========================================================
    // FIND EXISTING NOTES COMPLETE BUTTON
    // ========================================================

    function findContinueButton() {

        const elements = [
            ...document.querySelectorAll(
                "button, a"
            )
        ];

        return elements.find(
            element => {

                const text = (
                    element.textContent
                    || ""
                )
                    .trim()
                    .toLowerCase();

                return (
                    text.includes("continue learning")
                    ||
                    text === "continue"
                );
            }
        ) || null;
    }


    function findNotesCompleteArea(
        continueButton
    ) {

        if (!continueButton) {
            return null;
        }

        let current = continueButton.parentElement;

        for (
            let level = 0;
            level < 7 && current;
            level += 1
        ) {

            const content = (
                current.textContent
                || ""
            ).toLowerCase();

            if (
                content.includes("notes complete")
            ) {
                return current;
            }

            current = current.parentElement;
        }

        return continueButton.parentElement;
    }


    // ========================================================
    // NEXT BUTTON
    // Preserve existing navigation behaviour.
    // ========================================================

    function configureNextButton(
        button
    ) {

        if (!button) {
            return;
        }

        button.textContent =
            "Next → Video";

        button.classList.add(
            "personalized-notes-next-btn"
        );


        /*
            We DO NOT replace the existing onclick/href.
            Current Notes page already knows its correct next flow.

            We only log that the student needed the next resource.
        */

        button.addEventListener(
            "pointerdown",
            () => {

                saveEvent("next");

            },
            {
                capture: true
            }
        );
    }


    // ========================================================
    // UNDERSTOOD BUTTON
    // ========================================================

    function createUnderstoodButton(
        topicId,
        statusElement
    ) {

        const button = document.createElement(
            "button"
        );

        button.type = "button";

        button.className =
            "personalized-notes-understood-btn";

        button.textContent =
            "✓ I Understood → Next Topic";


        button.addEventListener(
            "click",
            async () => {

                button.disabled = true;

                button.textContent =
                    "Saving your learning preference...";


                if (statusElement) {

                    statusElement.textContent =
                        "Saving: Notes helped you understand this topic.";
                }


                const result = await saveEvent(
                    "understood"
                );


                if (statusElement) {

                    statusElement.classList.add(
                        "personalized-notes-success"
                    );

                    if (
                        result
                        &&
                        result.preferred_resource_label
                    ) {

                        statusElement.textContent =
                            (
                                "✓ Learning preference saved. "
                                +
                                `Current preferred mode: ${result.preferred_resource_label}.`
                            );

                    } else {

                        statusElement.textContent =
                            "✓ Saved: you understood this topic through Notes.";
                    }
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


        return button;
    }


    // ========================================================
    // INSTALL INSIDE EXISTING NOTES COMPLETE CARD
    // ========================================================

    function installPersonalizedActions() {

        if (
            document.querySelector(
                ".personalized-notes-understood-btn"
            )
        ) {
            return true;
        }


        const topicId = getTopicId();

        if (!topicId) {
            return false;
        }


        const continueButton = findContinueButton();

        if (!continueButton) {
            return false;
        }


        const completeArea = findNotesCompleteArea(
            continueButton
        );


        configureNextButton(
            continueButton
        );


        const existingParent =
            continueButton.parentElement;


        if (!existingParent) {
            return false;
        }


        existingParent.classList.add(
            "personalized-notes-actions"
        );


        const status = document.createElement(
            "div"
        );

        status.className =
            "personalized-notes-status";

        status.textContent =
            (
                "If Notes were enough, stop here. "
                +
                "Otherwise continue to Video."
            );


        const understoodButton =
            createUnderstoodButton(
                topicId,
                status
            );


        existingParent.appendChild(
            understoodButton
        );

        existingParent.appendChild(
            status
        );


        console.log(
            "[My Campus] Notes personalization ready."
        );


        return true;
    }


    // ========================================================
    // INITIALIZATION
    // ========================================================

    async function init() {

        /*
            Always record Notes started.
            UI rendering does NOT depend on API success.
        */

        saveEvent("started");


        if (
            installPersonalizedActions()
        ) {
            return;
        }


        /*
            Notes content may be rendered asynchronously,
            so observe until the Notes Complete card appears.
        */

        const observer = new MutationObserver(
            () => {

                if (
                    installPersonalizedActions()
                ) {

                    observer.disconnect();
                }
            }
        );


        observer.observe(
            document.body,
            {
                childList: true,
                subtree: true
            }
        );


        window.setTimeout(
            () => {

                observer.disconnect();

                installPersonalizedActions();

            },
            10000
        );
    }


    if (
        document.readyState === "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            init
        );

    } else {

        init();
    }

})();
