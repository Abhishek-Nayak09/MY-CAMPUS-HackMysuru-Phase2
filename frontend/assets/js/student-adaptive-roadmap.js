(function () {

    "use strict";


    const API_BASE =
        "http://127.0.0.1:8000";


    const RESOURCE_ORDER = [
        "notes",
        "video",
        "interactive",
        "game",
        "ai_tutor",
        "faculty"
    ];


    const RESOURCE_META = {

        notes: {
            icon: "📘",
            label: "Notes"
        },

        video: {
            icon: "▶️",
            label: "Video"
        },

        interactive: {
            icon: "🧊",
            label: "3D Interactive"
        },

        game: {
            icon: "🎮",
            label: "Game"
        },

        ai_tutor: {
            icon: "🤖",
            label: "AI Tutor"
        },

        faculty: {
            icon: "👨‍🏫",
            label: "Faculty"
        }

    };


    let activeTopicId =
        null;


    let latestData =
        null;


    // ========================================================
    // STUDENT ID
    // ========================================================

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


            return Number(
                user.id
                ||
                user.user_id
                ||
                user.userId
                ||
                0
            ) || null;


        } catch (error) {

            return null;
        }
    }


    // ========================================================
    // TOPIC ID
    // ========================================================

    function topicFromQuery() {

        const params =
            new URLSearchParams(
                window.location.search
            );


        const keys = [
            "next_topic_id",
            "open_ai_topic",
            "open_faculty_topic",
            "topic_id"
        ];


        for (
            const key
            of keys
        ) {

            const value =
                Number(
                    params.get(
                        key
                    )
                );


            if (
                value >= 1
                &&
                value <= 10
            ) {

                return value;
            }
        }


        return null;
    }


    function topicFromStorage() {

        const value =
            Number(
                localStorage.getItem(
                    "my_campus_last_topic"
                )
            );


        if (
            value >= 1
            &&
            value <= 10
        ) {

            return value;
        }


        return null;
    }


    function topicFromCards() {

        const cards =
            document.querySelectorAll(
                ".topic-card"
            );


        for (
            const card
            of cards
        ) {

            if (
                card.classList.contains(
                    "topic-locked"
                )
            ) {

                continue;
            }


            const index =
                card.querySelector(
                    ".topic-index"
                );


            if (!index) {

                continue;
            }


            const match =
                index.textContent.match(
                    /TOPIC\s+(\d+)/i
                );


            if (match) {

                return Number(
                    match[1]
                );
            }
        }


        return null;
    }


    function resolveTopicId() {

        return (
            topicFromQuery()
            ||
            topicFromStorage()
            ||
            topicFromCards()
            ||
            1
        );
    }


    // ========================================================
    // STYLES
    // ========================================================

    function installStyles() {

        if (
            document.getElementById(
                "adaptive-roadmap-style"
            )
        ) {

            return;
        }


        const style =
            document.createElement(
                "style"
            );


        style.id =
            "adaptive-roadmap-style";


        style.textContent = `

            .adaptive-roadmap-shell {
                margin: 18px 0 24px;
                padding: 20px;
                border: 1px solid #e7e3ff;
                border-radius: 22px;
                background:
                    linear-gradient(
                        135deg,
                        #ffffff,
                        #faf9ff
                    );
                box-shadow:
                    0 12px 34px
                    rgba(65, 51, 140, .07);
            }

            .adaptive-roadmap-top {
                display: flex;
                justify-content: space-between;
                gap: 20px;
                align-items: flex-start;
                margin-bottom: 17px;
            }

            .adaptive-roadmap-badge {
                display: inline-flex;
                padding: 6px 10px;
                border-radius: 999px;
                background: #f0edff;
                color: #6655e8;
                font-size: 10px;
                font-weight: 900;
                letter-spacing: .6px;
            }

            .adaptive-roadmap-title {
                margin: 8px 0 4px;
                color: #23283a;
                font-size: 18px;
            }

            .adaptive-roadmap-subtitle {
                margin: 0;
                color: #7b8192;
                font-size: 12px;
                line-height: 1.5;
            }

            .adaptive-adapter {
                min-width: 255px;
                max-width: 340px;
                padding: 12px 14px;
                border: 1px solid #d9d4ff;
                border-radius: 15px;
                background: #f7f5ff;
            }

            .adaptive-adapter small {
                display: block;
                color: #7768e8;
                font-size: 10px;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: .5px;
            }

            .adaptive-adapter strong {
                display: block;
                margin-top: 5px;
                color: #282b3c;
                font-size: 13px;
            }

            .adaptive-adapter p {
                margin: 5px 0 0;
                color: #777d8d;
                font-size: 11px;
                line-height: 1.45;
            }

            .adaptive-roadmap-track {
                display: grid;
                grid-template-columns:
                    repeat(6, minmax(105px, 1fr));
                gap: 8px;
            }

            .adaptive-step {
                position: relative;
                padding: 12px 8px;
                border: 1px solid #ece9f7;
                border-radius: 14px;
                background: #ffffff;
                text-align: center;
                transition:
                    transform .15s ease,
                    border-color .15s ease,
                    box-shadow .15s ease;
            }

            .adaptive-step::after {
                content: "→";
                position: absolute;
                right: -9px;
                top: 50%;
                transform: translateY(-50%);
                color: #bbb7cf;
                font-weight: 900;
                z-index: 2;
            }

            .adaptive-step:last-child::after {
                display: none;
            }

            .adaptive-step-icon {
                font-size: 20px;
            }

            .adaptive-step-label {
                margin-top: 5px;
                color: #33384a;
                font-size: 11px;
                font-weight: 850;
            }

            .adaptive-step-status {
                margin-top: 4px;
                color: #989daf;
                font-size: 9px;
                text-transform: uppercase;
                font-weight: 800;
            }

            .adaptive-step.started {
                border-color: #c9c1ff;
                background: #faf9ff;
            }

            .adaptive-step.completed {
                border-color: #a7d9bd;
                background: #f5fff9;
            }

            .adaptive-step.understood {
                border-color: #6fd49a;
                background: #edfff5;
                box-shadow:
                    0 7px 18px
                    rgba(41, 170, 96, .10);
            }

            .adaptive-step.escalated {
                border-color: #f3bf75;
                background: #fff9ee;
            }

            .adaptive-step.current {
                border-color: #7968ef;
                box-shadow:
                    0 0 0 2px
                    rgba(121, 104, 239, .10);
            }

            .adaptive-step.recommended {
                border-color: #7968ef;
                background:
                    linear-gradient(
                        145deg,
                        #f4f1ff,
                        #ffffff
                    );
            }

            .adaptive-recommended-tag {
                display: inline-block;
                margin-top: 5px;
                padding: 3px 6px;
                border-radius: 999px;
                background: #7867ef;
                color: white;
                font-size: 8px;
                font-weight: 900;
            }

            @media (max-width: 900px) {

                .adaptive-roadmap-top {
                    flex-direction: column;
                }

                .adaptive-adapter {
                    width: 100%;
                    max-width: none;
                }

                .adaptive-roadmap-track {
                    grid-template-columns:
                        repeat(3, 1fr);
                }

                .adaptive-step::after {
                    display: none;
                }
            }

            @media (max-width: 560px) {

                .adaptive-roadmap-track {
                    grid-template-columns:
                        repeat(2, 1fr);
                }
            }
        `;


        document.head.appendChild(
            style
        );
    }


    // ========================================================
    // HOST
    // ========================================================

    function ensureHost() {

        let host =
            document.getElementById(
                "adaptiveLearningRoadmap"
            );


        if (host) {

            return host;
        }


        const hero =
            document.querySelector(
                ".hero"
            );


        if (!hero) {

            return null;
        }


        host =
            document.createElement(
                "section"
            );


        host.id =
            "adaptiveLearningRoadmap";


        host.className =
            "adaptive-roadmap-shell";


        hero.insertAdjacentElement(
            "afterend",
            host
        );


        return host;
    }


    // ========================================================
    // STATUS LABEL
    // ========================================================

    function statusLabel(
        status
    ) {

        const map = {

            not_started:
                "Not started",

            started:
                "In progress",

            completed:
                "Completed",

            understood:
                "Understood",

            escalated:
                "Escalated"
        };


        return (
            map[
                status
            ]
            ||
            "Not started"
        );
    }


    // ========================================================
    // RENDER
    // ========================================================

    function render(
        data
    ) {

        latestData =
            data;


        const host =
            ensureHost();


        if (!host) {

            return;
        }


        const topic =
            data.topic
            ||
            {
                id:
                    activeTopicId,

                title:
                    `Topic ${activeTopicId}`
            };


        const personalization =
            data.personalization
            ||
            {};


        const preferred =
            personalization
                .preferred_resource;


        const preferredLabel =
            personalization
                .preferred_resource_label;


        const confidence =
            Math.round(
                Number(
                    personalization
                        .preference_confidence
                    ||
                    0
                )
                *
                100
            );


        const current =
            data.current_resource
            ||
            "notes";


        host.innerHTML =
            "";


        const top =
            document.createElement(
                "div"
            );


        top.className =
            "adaptive-roadmap-top";


        const copy =
            document.createElement(
                "div"
            );


        copy.innerHTML = `
            <span class="adaptive-roadmap-badge">
                LIVE LEARNING ROADMAP
            </span>

            <h2 class="adaptive-roadmap-title">
                Topic ${topic.id} · ${topic.title}
            </h2>

            <p class="adaptive-roadmap-subtitle">
                Your journey updates as you learn.
                You can move forward whenever you understand the concept.
            </p>
        `;


        const adapter =
            document.createElement(
                "div"
            );


        adapter.className =
            "adaptive-adapter";


        if (preferredLabel) {

            adapter.innerHTML = `
                <small>
                    ✨ Personalized AI Adapter
                </small>

                <strong>
                    Best-fit mode:
                    ${preferredLabel}
                </strong>

                <p>
                    MY CAMPUS learned this from your previous
                    successful learning attempts.
                    Confidence: ${confidence}%.
                </p>
            `;

        } else {

            adapter.innerHTML = `
                <small>
                    ✨ Personalized AI Adapter
                </small>

                <strong>
                    Learning your style
                </strong>

                <p>
                    Use the resources normally.
                    When you choose “I Understood”, MY CAMPUS
                    learns which method works best for you.
                </p>
            `;
        }


        top.append(
            copy,
            adapter
        );


        const track =
            document.createElement(
                "div"
            );


        track.className =
            "adaptive-roadmap-track";


        const roadmap =
            Array.isArray(
                data.roadmap
            )
                ? data.roadmap
                : [];


        RESOURCE_ORDER.forEach(
            resource => {

                const meta =
                    RESOURCE_META[
                        resource
                    ];


                const progress =
                    roadmap.find(
                        item =>
                            item.resource_type
                            === resource
                    );


                const status =
                    progress?.status
                    ||
                    "not_started";


                const step =
                    document.createElement(
                        "div"
                    );


                step.className =
                    "adaptive-step";


                step.classList.add(
                    status
                );


                if (
                    current ===
                    resource
                ) {

                    step.classList.add(
                        "current"
                    );
                }


                if (
                    preferred ===
                    resource
                ) {

                    step.classList.add(
                        "recommended"
                    );
                }


                step.innerHTML = `
                    <div class="adaptive-step-icon">
                        ${meta.icon}
                    </div>

                    <div class="adaptive-step-label">
                        ${meta.label}
                    </div>

                    <div class="adaptive-step-status">
                        ${statusLabel(status)}
                    </div>

                    ${
                        preferred === resource

                            ? `
                                <span class="adaptive-recommended-tag">
                                    RECOMMENDED
                                </span>
                            `

                            : ""
                    }
                `;


                track.appendChild(
                    step
                );
            }
        );


        host.append(
            top,
            track
        );
    }


    // ========================================================
    // LOAD
    // ========================================================

    async function refresh() {

        const studentId =
            getStudentId();


        activeTopicId =
            resolveTopicId();


        if (
            !studentId
            ||
            !activeTopicId
        ) {

            return;
        }


        localStorage.setItem(
            "my_campus_last_topic",
            String(
                activeTopicId
            )
        );


        try {

            const response =
                await fetch(
                    `${API_BASE}/personalization/topic/${studentId}/${activeTopicId}`
                );


            if (!response.ok) {

                throw new Error(
                    `HTTP ${response.status}`
                );
            }


            const data =
                await response.json();


            render(
                data
            );


        } catch (error) {

            console.warn(
                "Adaptive roadmap unavailable:",
                error
            );
        }
    }


    // ========================================================
    // FOLLOW TOPIC CARD CLICKS
    // ========================================================

    document.addEventListener(
        "click",
        event => {

            const button =
                event.target.closest(
                    ".method-btn"
                );


            if (!button) {

                return;
            }


            const card =
                button.closest(
                    ".topic-card"
                );


            const index =
                card?.querySelector(
                    ".topic-index"
                );


            if (!index) {

                return;
            }


            const match =
                index.textContent.match(
                    /TOPIC\s+(\d+)/i
                );


            if (!match) {

                return;
            }


            const topicId =
                Number(
                    match[1]
                );


            if (
                topicId >= 1
                &&
                topicId <= 10
            ) {

                localStorage.setItem(
                    "my_campus_last_topic",
                    String(
                        topicId
                    )
                );
            }

        },
        true
    );


    // ========================================================
    // START
    // ========================================================

    function start() {

        installStyles();


        const observer =
            new MutationObserver(
                () => {

                    if (
                        document.querySelector(
                            ".topic-card"
                        )
                    ) {

                        observer.disconnect();

                        refresh();
                    }
                }
            );


        const path =
            document.getElementById(
                "learningPath"
            );


        if (path) {

            observer.observe(
                path,
                {
                    childList:
                        true,

                    subtree:
                        true
                }
            );
        }


        if (
            document.querySelector(
                ".topic-card"
            )
        ) {

            refresh();
        }
    }


    window.refreshAdaptiveRoadmap =
        refresh;


    window.addEventListener(
        "pageshow",
        refresh
    );


    document.addEventListener(
        "visibilitychange",
        () => {

            if (
                document.visibilityState
                === "visible"
            ) {

                refresh();
            }
        }
    );


    window.addEventListener(
        "faculty-doubt-sent",
        refresh
    );


    if (
        document.readyState
        === "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            start
        );

    } else {

        start();
    }

})();