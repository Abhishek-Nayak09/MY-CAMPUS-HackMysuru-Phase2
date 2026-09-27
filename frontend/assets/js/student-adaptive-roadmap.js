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
        },

        next_topic: {
            icon: "➡️",
            label: "Next Topic"
        }

    };


    let activeTopicId =
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
    // SAFE HTML
    // ========================================================

    function escapeHtml(
        value
    ) {

        return String(
            value ?? ""
        )
        .replaceAll(
            "&",
            "&amp;"
        )
        .replaceAll(
            "<",
            "&lt;"
        )
        .replaceAll(
            ">",
            "&gt;"
        )
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );
    }


    // ========================================================
    // STYLES
    // ========================================================

    function installStyles() {

        if (
            document.getElementById(
                "adaptive-roadmap-style-v21"
            )
        ) {

            return;
        }


        const style =
            document.createElement(
                "style"
            );


        style.id =
            "adaptive-roadmap-style-v21";


        style.textContent = `

            .adaptive-roadmap-shell {
                margin: 18px 0 24px;
                padding: 20px;
                border: 1px solid #e6e2ff;
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
                display: grid;
                grid-template-columns:
                    minmax(0, 1.1fr)
                    minmax(300px, .9fr);
                gap: 18px;
                align-items: stretch;
            }

            .adaptive-roadmap-badge {
                display: inline-flex;
                padding: 6px 10px;
                border-radius: 999px;
                background: #efedff;
                color: #6555e8;
                font-size: 10px;
                font-weight: 900;
                letter-spacing: .6px;
            }

            .adaptive-roadmap-title {
                margin: 9px 0 5px;
                color: #23283a;
                font-size: 19px;
            }

            .adaptive-roadmap-subtitle {
                margin: 0;
                max-width: 720px;
                color: #7b8192;
                font-size: 12px;
                line-height: 1.55;
            }

            .adaptive-engine-card {
                padding: 15px;
                border: 1px solid #d9d3ff;
                border-radius: 17px;
                background:
                    linear-gradient(
                        145deg,
                        #f6f4ff,
                        #ffffff
                    );
            }

            .adaptive-engine-topline {
                display: flex;
                justify-content: space-between;
                gap: 10px;
                align-items: center;
            }

            .adaptive-engine-label {
                color: #6959e8;
                font-size: 10px;
                font-weight: 950;
                letter-spacing: .5px;
                text-transform: uppercase;
            }

            .adaptive-engine-version {
                padding: 4px 7px;
                border-radius: 999px;
                background: #ebe7ff;
                color: #7465df;
                font-size: 9px;
                font-weight: 900;
            }

            .adaptive-next-action {
                margin-top: 9px;
                color: #252a3a;
                font-size: 16px;
                font-weight: 900;
            }

            .adaptive-reason {
                margin-top: 6px;
                color: #757b8c;
                font-size: 11px;
                line-height: 1.5;
            }

            .adaptive-confidence-row {
                display: flex;
                justify-content: space-between;
                gap: 8px;
                margin-top: 11px;
                color: #6d7283;
                font-size: 10px;
                font-weight: 800;
            }

            .adaptive-confidence-track {
                height: 7px;
                margin-top: 5px;
                overflow: hidden;
                border-radius: 999px;
                background: #e9e7f3;
            }

            .adaptive-confidence-fill {
                height: 100%;
                border-radius: inherit;
                background:
                    linear-gradient(
                        90deg,
                        #7968ef,
                        #9e91ff
                    );
            }

            .adaptive-summary-grid {
                display: grid;
                grid-template-columns:
                    repeat(4, minmax(0, 1fr));
                gap: 8px;
                margin-top: 15px;
            }

            .adaptive-summary-card {
                padding: 10px;
                border: 1px solid #ece9f7;
                border-radius: 13px;
                background: #ffffff;
            }

            .adaptive-summary-card small {
                display: block;
                color: #969bad;
                font-size: 8px;
                font-weight: 900;
                text-transform: uppercase;
            }

            .adaptive-summary-card strong {
                display: block;
                margin-top: 4px;
                color: #33384a;
                font-size: 12px;
            }

            .adaptive-roadmap-track {
                display: grid;
                grid-template-columns:
                    repeat(6, minmax(105px, 1fr));
                gap: 8px;
                margin-top: 17px;
            }

            .adaptive-step {
                position: relative;
                padding: 12px 8px;
                border: 1px solid #ece9f7;
                border-radius: 14px;
                background: #ffffff;
                text-align: center;
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

            .adaptive-step.preferred {
                border-color: #7968ef;
                background:
                    linear-gradient(
                        145deg,
                        #f4f1ff,
                        #ffffff
                    );
            }

            .adaptive-step.low-effectiveness {
                border-color: #f0c9c9;
                background: #fff9f9;
            }

            .adaptive-tag {
                display: inline-block;
                margin-top: 5px;
                padding: 3px 6px;
                border-radius: 999px;
                font-size: 8px;
                font-weight: 900;
            }

            .adaptive-tag.preferred-tag {
                background: #7867ef;
                color: #ffffff;
            }

            .adaptive-tag.low-tag {
                background: #fff0f0;
                color: #b54e4e;
            }

            .adaptive-intelligence-row {
                display: grid;
                grid-template-columns:
                    minmax(0, 1fr)
                    minmax(280px, .8fr);
                gap: 12px;
                margin-top: 14px;
            }

            .adaptive-ranking,
            .adaptive-signals {
                padding: 14px;
                border: 1px solid #ece9f7;
                border-radius: 15px;
                background: #ffffff;
            }

            .adaptive-section-title {
                color: #3a4052;
                font-size: 11px;
                font-weight: 950;
                text-transform: uppercase;
                letter-spacing: .4px;
            }

            .adaptive-rank-row {
                display: grid;
                grid-template-columns:
                    115px
                    minmax(80px, 1fr)
                    48px;
                gap: 8px;
                align-items: center;
                margin-top: 9px;
            }

            .adaptive-rank-name {
                color: #555b6c;
                font-size: 10px;
                font-weight: 800;
            }

            .adaptive-rank-track {
                height: 7px;
                overflow: hidden;
                border-radius: 999px;
                background: #eceaf4;
            }

            .adaptive-rank-fill {
                height: 100%;
                border-radius: inherit;
                background: #8170ef;
            }

            .adaptive-rank-score {
                color: #595f71;
                font-size: 9px;
                font-weight: 900;
                text-align: right;
            }

            .adaptive-signal {
                margin-top: 8px;
                padding: 8px 10px;
                border-radius: 10px;
                background: #f7f6fb;
                color: #6f7585;
                font-size: 10px;
                line-height: 1.45;
            }

            .adaptive-signal.warning {
                background: #fff7e9;
                color: #8a641e;
            }

            .adaptive-signal.good {
                background: #effbf4;
                color: #377954;
            }

            .adaptive-signal.low {
                background: #fff2f2;
                color: #a24e4e;
            }

            @media (max-width: 1000px) {

                .adaptive-roadmap-top,
                .adaptive-intelligence-row {
                    grid-template-columns: 1fr;
                }

                .adaptive-summary-grid {
                    grid-template-columns:
                        repeat(2, 1fr);
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

                .adaptive-summary-grid,
                .adaptive-roadmap-track {
                    grid-template-columns:
                        repeat(2, 1fr);
                }

                .adaptive-rank-row {
                    grid-template-columns:
                        95px
                        1fr
                        40px;
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
    // STATUS
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
        roadmapData,
        adaptiveData
    ) {

        const host =
            ensureHost();


        if (!host) {

            return;
        }


        const decision =
            adaptiveData?.decision
            ||
            adaptiveData?.adaptive_profile
            ||
            {};


        const topic =
            adaptiveData?.topic
            ||
            roadmapData?.topic
            ||
            {
                id:
                    activeTopicId,

                title:
                    `Topic ${activeTopicId}`
            };


        const learner =
            decision.learner_model
            ||
            {};


        const recommendation =
            decision.recommendation
            ||
            {};


        const support =
            decision.support
            ||
            {};


        const summary =
            decision.history_summary
            ||
            {};


        const currentTopic =
            decision.current_topic
            ||
            {};


        const preferred =
            learner.preferred_resource
            ||
            null;


        const confidence =
            Math.round(
                Number(
                    learner.confidence
                    ||
                    recommendation.confidence
                    ||
                    0
                )
                *
                100
            );


        const current =
            roadmapData?.current_resource
            ||
            "notes";


        const roadmap =
            Array.isArray(
                roadmapData?.roadmap
            )
                ? roadmapData.roadmap
                : [];


        const lowEffectiveness =
            new Set(

                Array.isArray(
                    decision.low_effectiveness_resources
                )

                    ? decision
                        .low_effectiveness_resources
                        .map(
                            item =>
                                item.resource_type
                        )

                    : []
            );


        const recommendationReasons =
            Array.isArray(
                recommendation.reasons
            )
                ? recommendation.reasons
                : [];


        const firstReason =
            recommendationReasons[0]
            ||
            "MY CAMPUS is still learning from your activity.";


        host.innerHTML = `

            <div class="adaptive-roadmap-top">

                <div>

                    <span class="adaptive-roadmap-badge">
                        LIVE ADAPTIVE LEARNING ROADMAP
                    </span>

                    <h2 class="adaptive-roadmap-title">
                        Topic ${escapeHtml(topic.id)}
                        ·
                        ${escapeHtml(topic.title)}
                    </h2>

                    <p class="adaptive-roadmap-subtitle">
                        This roadmap is not fixed.
                        MY CAMPUS continuously updates the next learning
                        action using your previous successes, retries,
                        assessment gaps and support history.
                    </p>


                    <div class="adaptive-summary-grid">

                        <div class="adaptive-summary-card">

                            <small>
                                Learning state
                            </small>

                            <strong>
                                ${escapeHtml(
                                    currentTopic.learning_state
                                    ||
                                    "Learning"
                                )}
                            </strong>

                        </div>


                        <div class="adaptive-summary-card">

                            <small>
                                Best-fit mode
                            </small>

                            <strong>
                                ${escapeHtml(
                                    learner.preferred_resource_label
                                    ||
                                    "Learning profile"
                                )}
                            </strong>

                        </div>


                        <div class="adaptive-summary-card">

                            <small>
                                Topics understood
                            </small>

                            <strong>
                                ${Number(
                                    summary.topics_understood
                                    ||
                                    0
                                )}
                            </strong>

                        </div>


                        <div class="adaptive-summary-card">

                            <small>
                                Concept gaps
                            </small>

                            <strong>
                                ${Number(
                                    summary.concept_gap_count
                                    ||
                                    0
                                )}
                            </strong>

                        </div>

                    </div>

                </div>


                <div class="adaptive-engine-card">

                    <div class="adaptive-engine-topline">

                        <div class="adaptive-engine-label">
                            ✨ Adaptive Intelligence
                        </div>

                        <div class="adaptive-engine-version">
                            ENGINE v2.1
                        </div>

                    </div>


                    <div class="adaptive-next-action">

                        Next action:
                        ${escapeHtml(
                            recommendation.label
                            ||
                            "Continue Learning"
                        )}

                    </div>


                    <div class="adaptive-reason">

                        ${escapeHtml(
                            firstReason
                        )}

                    </div>


                    <div class="adaptive-confidence-row">

                        <span>
                            Decision confidence
                        </span>

                        <span>
                            ${confidence}%
                            ·
                            ${escapeHtml(
                                recommendation.confidence_label
                                ||
                                "learning"
                            )}
                        </span>

                    </div>


                    <div class="adaptive-confidence-track">

                        <div
                            class="adaptive-confidence-fill"
                            style="
                                width:
                                ${Math.max(
                                    0,
                                    Math.min(
                                        100,
                                        confidence
                                    )
                                )}%;
                            "
                        ></div>

                    </div>


                    <div class="adaptive-signal good">

                        Preferred learning mode:
                        <b>
                            ${escapeHtml(
                                learner.preferred_resource_label
                                ||
                                "Still learning"
                            )}
                        </b>

                    </div>


                    ${
                        support.reason

                            ? `
                                <div class="adaptive-signal">
                                    ${escapeHtml(
                                        support.reason
                                    )}
                                </div>
                            `

                            : ""
                    }

                </div>

            </div>


            <div
                id="adaptiveRoadmapTrack"
                class="adaptive-roadmap-track"
            ></div>


            <div class="adaptive-intelligence-row">

                <div class="adaptive-ranking">

                    <div class="adaptive-section-title">
                        Learning Mode Evidence
                    </div>

                    <div id="adaptiveRankingRows">
                    </div>

                </div>


                <div class="adaptive-signals">

                    <div class="adaptive-section-title">
                        Engine Signals
                    </div>

                    <div id="adaptiveSignalRows">
                    </div>

                </div>

            </div>
        `;


        // ====================================================
        // ROADMAP
        // ====================================================

        const track =
            document.getElementById(
                "adaptiveRoadmapTrack"
            );


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
                            ===
                            resource
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
                        "preferred"
                    );
                }


                if (
                    lowEffectiveness.has(
                        resource
                    )
                ) {

                    step.classList.add(
                        "low-effectiveness"
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
                        preferred ===
                        resource

                            ? `
                                <span
                                    class="adaptive-tag preferred-tag"
                                >
                                    BEST FIT
                                </span>
                            `

                            : ""
                    }

                    ${
                        lowEffectiveness.has(
                            resource
                        )

                            ? `
                                <span
                                    class="adaptive-tag low-tag"
                                >
                                    LOW EFFECTIVENESS
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


        // ====================================================
        // RANKING
        // ====================================================

        const rankingRoot =
            document.getElementById(
                "adaptiveRankingRows"
            );


        const ranking =
            Array.isArray(
                learner.ranking
            )
                ? learner.ranking
                : [];


        if (!ranking.length) {

            rankingRoot.innerHTML = `

                <div class="adaptive-signal">
                    Not enough history yet.
                    Continue learning normally and the engine
                    will build your profile.
                </div>
            `;

        } else {

            ranking.forEach(
                item => {

                    const score =
                        Math.max(
                            0,
                            Math.min(
                                100,
                                Number(
                                    item.adaptive_score
                                    ||
                                    0
                                )
                            )
                        );


                    const row =
                        document.createElement(
                            "div"
                        );


                    row.className =
                        "adaptive-rank-row";


                    row.innerHTML = `

                        <div class="adaptive-rank-name">
                            ${escapeHtml(
                                item.label
                            )}
                        </div>

                        <div class="adaptive-rank-track">

                            <div
                                class="adaptive-rank-fill"
                                style="
                                    width:
                                    ${score}%;
                                "
                            ></div>

                        </div>

                        <div class="adaptive-rank-score">
                            ${score.toFixed(0)}
                        </div>
                    `;


                    rankingRoot.appendChild(
                        row
                    );
                }
            );
        }


        // ====================================================
        // SIGNALS
        // ====================================================

        const signalRoot =
            document.getElementById(
                "adaptiveSignalRows"
            );


        const signals = [];


        recommendationReasons.forEach(
            reason => {

                signals.push({
                    type:
                        "normal",

                    text:
                        reason
                });
            }
        );


        if (
            recommendation.exploration_label
        ) {

            signals.push({

                type:
                    "normal",

                text:
                    (
                        "Exploration suggestion: "
                        +
                        recommendation
                            .exploration_label
                    )
            });
        }


        if (
            Array.isArray(
                decision.active_concept_gaps
            )
        ) {

            decision
            .active_concept_gaps
            .slice(
                0,
                3
            )
            .forEach(
                gap => {

                    signals.push({

                        type:
                            "warning",

                        text:
                            (
                                `Weak concept: ${
                                    gap.concept
                                    ||
                                    "Concept gap"
                                }`
                            )
                    });
                }
            );
        }


        if (
            Array.isArray(
                decision.low_effectiveness_resources
            )
        ) {

            decision
            .low_effectiveness_resources
            .forEach(
                item => {

                    signals.push({

                        type:
                            "low",

                        text:
                            (
                                `${
                                    item.label
                                    ||
                                    item.resource_type
                                } is currently showing low effectiveness.`
                            )
                    });
                }
            );
        }


        if (
            Array.isArray(
                decision.data_quality_signals
            )
        ) {

            decision
            .data_quality_signals
            .forEach(
                item => {

                    signals.push({

                        type:
                            "warning",

                        text:
                            item.message
                    });
                }
            );
        }


        if (!signals.length) {

            signals.push({

                type:
                    "normal",

                text:
                    "No special difficulty signals detected for this topic."
            });
        }


        signalRoot.innerHTML =
            "";


        signals
        .slice(
            0,
            6
        )
        .forEach(
            signal => {

                const box =
                    document.createElement(
                        "div"
                    );


                box.className =
                    (
                        "adaptive-signal "
                        +
                        signal.type
                    );


                box.textContent =
                    signal.text;


                signalRoot.appendChild(
                    box
                );
            }
        );
    }


    // ========================================================
    // LOAD BOTH ENGINES
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

            const [
                roadmapResponse,
                adaptiveResponse
            ] =
                await Promise.all([

                    fetch(
                        `${API_BASE}/personalization/topic/${studentId}/${activeTopicId}`
                    ),

                    fetch(
                        `${API_BASE}/adaptive-intelligence/topic/${studentId}/${activeTopicId}`
                    )

                ]);


            if (
                !roadmapResponse.ok
                ||
                !adaptiveResponse.ok
            ) {

                throw new Error(
                    (
                        "Adaptive API error: "
                        +
                        roadmapResponse.status
                        +
                        " / "
                        +
                        adaptiveResponse.status
                    )
                );
            }


            const [
                roadmapData,
                adaptiveData
            ] =
                await Promise.all([

                    roadmapResponse.json(),

                    adaptiveResponse.json()

                ]);


            render(
                roadmapData,
                adaptiveData
            );


        } catch (error) {

            console.warn(
                "Adaptive Intelligence unavailable:",
                error
            );
        }
    }


    // ========================================================
    // FOLLOW RESOURCE BUTTON CLICKS
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

                activeTopicId =
                    topicId;


                localStorage.setItem(
                    "my_campus_last_topic",
                    String(
                        topicId
                    )
                );


                setTimeout(
                    refresh,
                    250
                );
            }
        }
    );


    // ========================================================
    // CUSTOM REFRESH EVENT
    // ========================================================

    window.addEventListener(

        "my-campus-personalization-updated",

        () => {

            refresh();
        }
    );


    // ========================================================
    // REFRESH WHEN RETURNING TO TAB
    // ========================================================

    window.addEventListener(

        "focus",

        () => {

            refresh();
        }
    );


    // ========================================================
    // INITIAL
    // ========================================================

    installStyles();


    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            refresh
        );

    } else {

        refresh();
    }


    // ========================================================
    // PUBLIC MANUAL REFRESH
    // ========================================================

    window.refreshMyCampusAdaptiveEngine =
        refresh;


})();