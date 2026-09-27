
(function () {

    "use strict";


    const API_BASE =
        "http://127.0.0.1:8000";


    const RESOURCE_META = {

        notes: {
            label:
                "Notes",

            icon:
                "📘",

            description:
                "Start from the normal reading and explanation flow."
        },


        video: {
            label:
                "Video",

            icon:
                "▶️",

            description:
                "Start with visual explanation through the topic video."
        },


        interactive: {
            label:
                "Interactive / Graphs",

            icon:
                "📊",

            description:
                "Start directly with graphs, simulations and interactive learning."
        },


        game: {
            label:
                "Game",

            icon:
                "🎮",

            description:
                "Start through game-based learning and practical interaction."
        },


        ai_tutor: {
            label:
                "AI Tutor",

            icon:
                "🤖",

            description:
                "Start with a personalized AI explanation for this topic."
        },


        faculty: {
            label:
                "Faculty",

            icon:
                "👨‍🏫",

            description:
                "Continue with faculty support for this topic."
        }

    };


    // ========================================================
    // QUERY
    // ========================================================

    function getNextTopicId() {

        const params =
            new URLSearchParams(
                window.location.search
            );


        const value =
            Number(
                params.get(
                    "next_topic_id"
                )
            );


        if (
            Number.isFinite(value)
            &&
            value > 0
            &&
            value <= 10
        ) {

            return value;
        }


        return null;
    }


    function getUnderstoodVia() {

        const params =
            new URLSearchParams(
                window.location.search
            );


        return (
            params.get(
                "understood_via"
            )
            ||
            ""
        )
            .trim()
            .toLowerCase();
    }


    // ========================================================
    // STUDENT ID
    // ========================================================

    function asPositiveNumber(
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


    function idFromObject(
        object
    ) {

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


        for (
            const candidate
            of candidates
        ) {

            const id =
                asPositiveNumber(
                    candidate
                );


            if (id) {

                return id;
            }
        }


        return null;
    }


    function scanStorage(
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

            const id =
                asPositiveNumber(
                    storage.getItem(
                        key
                    )
                );


            if (id) {

                return id;
            }
        }


        const objectKeys = [

            "myCampusUser",

            "currentUser",

            "loggedInUser",

            "user",

            "student",

            "portalUser"
        ];


        for (
            const key
            of objectKeys
        ) {

            const raw =
                storage.getItem(
                    key
                );


            if (!raw) {

                continue;
            }


            try {

                const parsed =
                    JSON.parse(
                        raw
                    );


                const id =
                    idFromObject(
                        parsed
                    );


                if (id) {

                    return id;
                }


            } catch (error) {

                // Ignore non JSON values.
            }
        }


        return null;
    }


    function getStudentIdSafe() {

        try {

            if (
                typeof window.getUserId
                === "function"
            ) {

                const id =
                    asPositiveNumber(
                        window.getUserId()
                    );


                if (id) {

                    return id;
                }
            }


        } catch (error) {

            console.warn(
                error
            );
        }


        try {

            const id =
                scanStorage(
                    window.localStorage
                );


            if (id) {

                return id;
            }


        } catch (error) {

            console.warn(
                error
            );
        }


        try {

            const id =
                scanStorage(
                    window.sessionStorage
                );


            if (id) {

                return id;
            }


        } catch (error) {

            console.warn(
                error
            );
        }


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
    // API
    // ========================================================

    async function getRecommendation(
        studentId,
        topicId
    ) {

        try {

            const response =
                await fetch(
                    `${API_BASE}/personalization/start-recommendation`,
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
                                    topicId
                            })
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
                "Recommendation API unavailable:",
                error
            );


            return null;
        }
    }


    // ========================================================
    // FIND TOPIC CARD
    // ========================================================

    function findTopicCard(
        topicId
    ) {

        const indexes =
            document.querySelectorAll(
                ".topic-index"
            );


        for (
            const indexElement
            of indexes
        ) {

            const text =
                (
                    indexElement.textContent
                    ||
                    ""
                )
                    .trim()
                    .toUpperCase();


            if (
                text
                ===
                `TOPIC ${topicId}`
            ) {

                return indexElement.closest(
                    ".topic-card"
                );
            }
        }


        return null;
    }


    function topicTitleFromCard(
        card,
        topicId
    ) {

        if (!card) {

            return (
                `Topic ${topicId}`
            );
        }


        const title =
            card.querySelector(
                ".topic-title"
            );


        return (
            title
            ?
            title.textContent.trim()
            :
            `Topic ${topicId}`
        );
    }


    // ========================================================
    // RESOURCE BUTTON CLICK
    // ========================================================

    function buttonClassForResource(
        resource
    ) {

        const map = {

            notes:
                "notes",

            video:
                "video",

            interactive:
                "interactive",

            game:
                "game",

            ai_tutor:
                "ai",

            faculty:
                "faculty"
        };


        return (
            map[
                resource
            ]
            ||
            "notes"
        );
    }


    function openResource(
        topicId,
        resource
    ) {

        const card =
            findTopicCard(
                topicId
            );


        if (!card) {

            alert(
                "Topic is still loading. Please try again."
            );

            return false;
        }


        const className =
            buttonClassForResource(
                resource
            );


        const button =
            card.querySelector(
                `.method-btn.${className}`
            );


        if (!button) {

            alert(
                "This learning resource is not available for this topic yet."
            );

            return false;
        }


        if (
            button.disabled
            ||
            button.classList.contains(
                "disabled"
            )
        ) {

            alert(
                "This topic/resource is currently locked."
            );

            return false;
        }


        removeNextTopicQuery();


        button.scrollIntoView({
            behavior:
                "smooth",

            block:
                "center"
        });


        window.setTimeout(
            () => {

                button.click();

            },
            180
        );


        return true;
    }


    // ========================================================
    // CLEAN QUERY AFTER CHOICE
    // ========================================================

    function removeNextTopicQuery() {

        const url =
            new URL(
                window.location.href
            );


        url.searchParams.delete(
            "next_topic_id"
        );


        url.searchParams.delete(
            "understood_via"
        );


        window.history.replaceState(
            {},
            "",
            url.pathname
            +
            url.search
            +
            url.hash
        );
    }


    // ========================================================
    // BUILD POPUP
    // ========================================================

    function buildPopup(
        topicId,
        topicTitle,
        recommendation
    ) {

        const old =
            document.getElementById(
                "nextTopicPersonalization"
            );


        if (old) {

            old.remove();
        }


        let recommendedResource =
            "interactive";


        let recommendationActive =
            false;


        if (
            recommendation
            &&
            recommendation.recommended
            &&
            recommendation.resource_type
            &&
            recommendation.resource_type
            !== "notes"
        ) {

            recommendedResource =
                recommendation.resource_type;


            recommendationActive =
                true;
        }


        const recommendedMeta =
            RESOURCE_META[
                recommendedResource
            ]
            ||
            RESOURCE_META.interactive;


        const understoodVia =
            getUnderstoodVia();


        const understoodLabel =
            RESOURCE_META[
                understoodVia
            ]
            ?.label
            ||
            null;


        const overlay =
            document.createElement(
                "div"
            );


        overlay.id =
            "nextTopicPersonalization";


        overlay.className =
            "next-topic-overlay open";


        const modal =
            document.createElement(
                "section"
            );


        modal.className =
            "next-topic-modal";


        // ----------------------------------------------------
        // HEADER
        // ----------------------------------------------------

        const head =
            document.createElement(
                "div"
            );


        head.className =
            "next-topic-head";


        const icon =
            document.createElement(
                "div"
            );


        icon.className =
            "next-topic-icon";


        icon.textContent =
            "✨";


        const heading =
            document.createElement(
                "div"
            );


        heading.className =
            "next-topic-heading";


        const kicker =
            document.createElement(
                "div"
            );


        kicker.className =
            "next-topic-kicker";


        kicker.textContent =
            `Topic ${topicId} ready`;


        const title =
            document.createElement(
                "h2"
            );


        title.textContent =
            topicTitle;


        const intro =
            document.createElement(
                "p"
            );


        intro.textContent =
            (
                "Choose how you want to begin. "
                +
                "My Campus will learn from what actually helps you understand."
            );


        heading.append(
            kicker,
            title,
            intro
        );


        const close =
            document.createElement(
                "button"
            );


        close.type =
            "button";


        close.className =
            "next-topic-close";


        close.textContent =
            "×";


        close.addEventListener(
            "click",
            () => {

                overlay.remove();
            }
        );


        head.append(
            icon,
            heading,
            close
        );


        // ----------------------------------------------------
        // BODY
        // ----------------------------------------------------

        const body =
            document.createElement(
                "div"
            );


        body.className =
            "next-topic-body";


        const insight =
            document.createElement(
                "div"
            );


        insight.className =
            "next-topic-insight";


        const insightLabel =
            document.createElement(
                "div"
            );


        insightLabel.className =
            "next-topic-insight-label";


        insightLabel.textContent =
            "Personalized learning suggestion";


        const insightText =
            document.createElement(
                "div"
            );


        insightText.className =
            "next-topic-insight-text";


        if (
            recommendationActive
        ) {

            insightText.textContent =
                (
                    "Your previous learning pattern suggests that "
                    +
                    `${recommendedMeta.label} may help you understand faster.`
                );

        } else {

            insightText.textContent =
                (
                    "Your learning profile is still developing. "
                    +
                    "You can start normally from Notes or try Interactive / Graphs."
                );
        }


        insight.append(
            insightLabel,
            insightText
        );


        if (understoodLabel) {

            const history =
                document.createElement(
                    "div"
                );


            history.className =
                "next-topic-history";


            history.textContent =
                (
                    "Previous topic was understood through: "
                    +
                    understoodLabel
                );


            insight.appendChild(
                history
            );
        }


        const question =
            document.createElement(
                "div"
            );


        question.className =
            "next-topic-question";


        question.textContent =
            "Where do you want to start?";


        const options =
            document.createElement(
                "div"
            );


        options.className =
            "next-topic-options";


        // ----------------------------------------------------
        // NORMAL NOTES OPTION
        // ----------------------------------------------------

        const normal =
            document.createElement(
                "button"
            );


        normal.type =
            "button";


        normal.className =
            "next-topic-option";


        normal.innerHTML = `
            <div class="next-topic-option-icon">
                📘
            </div>

            <div class="next-topic-option-title">
                Start Normally from Notes
            </div>

            <div class="next-topic-option-description">
                Follow the standard learning sequence from the beginning.
            </div>
        `;


        normal.addEventListener(
            "click",
            () => {

                openResource(
                    topicId,
                    "notes"
                );
            }
        );


        // ----------------------------------------------------
        // PERSONALIZED OPTION
        // ----------------------------------------------------

        const personalized =
            document.createElement(
                "button"
            );


        personalized.type =
            "button";


        personalized.className =
            "next-topic-option recommended";


        personalized.innerHTML = `
            <div class="next-topic-option-icon">
                ${recommendedMeta.icon}
            </div>

            <div class="next-topic-option-title">
                Start with ${recommendedMeta.label}
            </div>

            <div class="next-topic-option-description">
                ${recommendedMeta.description}
            </div>

            <div class="next-topic-recommended-chip">
                ${
                    recommendationActive
                    ?
                    "Recommended for you"
                    :
                    "Try another learning style"
                }
            </div>
        `;


        personalized.addEventListener(
            "click",
            () => {

                openResource(
                    topicId,
                    recommendedResource
                );
            }
        );


        options.append(
            normal,
            personalized
        );


        const footer =
            document.createElement(
                "div"
            );


        footer.className =
            "next-topic-footer";


        const footerNote =
            document.createElement(
                "div"
            );


        footerNote.className =
            "next-topic-footer-note";


        footerNote.textContent =
            (
                "Nothing is locked. You can still use "
                +
                "any learning resource later."
            );


        const stay =
            document.createElement(
                "button"
            );


        stay.type =
            "button";


        stay.className =
            "next-topic-skip";


        stay.textContent =
            "Stay on learning path";


        stay.addEventListener(
            "click",
            () => {

                overlay.remove();
            }
        );


        footer.append(
            footerNote,
            stay
        );


        body.append(
            insight,
            question,
            options,
            footer
        );


        modal.append(
            head,
            body
        );


        overlay.appendChild(
            modal
        );


        document.body.appendChild(
            overlay
        );
    }


    // ========================================================
    // WAIT UNTIL TOPIC CARDS ARE RENDERED
    // ========================================================

    function waitForTopicCard(
        topicId
    ) {

        return new Promise(
            resolve => {

                const immediate =
                    findTopicCard(
                        topicId
                    );


                if (immediate) {

                    resolve(
                        immediate
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
    // START
    // ========================================================

    async function init() {

        const topicId =
            getNextTopicId();


        if (!topicId) {

            return;
        }


        const studentId =
            getStudentIdSafe();


        if (!studentId) {

            console.warn(
                "Next topic personalization skipped: no student ID."
            );

            return;
        }


        const card =
            await waitForTopicCard(
                topicId
            );


        const topicTitle =
            topicTitleFromCard(
                card,
                topicId
            );


        const recommendation =
            await getRecommendation(
                studentId,
                topicId
            );


        buildPopup(
            topicId,
            topicTitle,
            recommendation
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
