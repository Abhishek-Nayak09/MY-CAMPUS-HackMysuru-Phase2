(function () {

    "use strict";


    const API =
        "http://127.0.0.1:8000";


    let user = null;


    try {

        user =
            JSON.parse(
                localStorage.getItem(
                    "myCampusUser"
                )
                ||
                "null"
            );

    } catch (error) {

        user = null;
    }


    if (
        !user
        ||
        user.role !== "faculty"
        ||
        user.faculty_role !== "hod"
    ) {

        return;
    }


    /* =========================================================
       FORCE HOD-ONLY VIEW
    ========================================================= */


    const professorDashboard =
        document.getElementById(
            "professorDashboard"
        );


    const hodDashboard =
        document.getElementById(
            "hodDashboard"
        );


    const resourceNav =
        document.getElementById(
            "resourceNav"
        );


    const ticketsNav =
        document.getElementById(
            "ticketsNav"
        );


    const analyticsNav =
        document.getElementById(
            "analyticsNav"
        );


    if (professorDashboard) {

        professorDashboard.style.display =
            "none";
    }


    if (hodDashboard) {

        hodDashboard.style.display =
            "block";
    }


    if (resourceNav) {

        resourceNav.style.display =
            "none";
    }


    if (ticketsNav) {

        ticketsNav.style.display =
            "none";
    }


    if (analyticsNav) {

        analyticsNav.style.display =
            "";
    }


    /* =========================================================
       HELPERS
    ========================================================= */


    function formatMinutes(
        minutes
    ) {

        const value =
            Number(
                minutes
            );


        if (
            !Number.isFinite(
                value
            )
            ||
            value < 0
        ) {

            return "-";
        }


        if (value < 1) {

            return "< 1 min";
        }


        if (value < 60) {

            return (
                Math.round(
                    value
                )
                + " min"
            );
        }


        const hours =
            Math.floor(
                value / 60
            );


        const remaining =
            Math.round(
                value % 60
            );


        if (!remaining) {

            return (
                hours
                + "h"
            );
        }


        return (
            hours
            + "h "
            + remaining
            + "m"
        );
    }


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


    async function loadOverview() {

        if (!user.access_token) {

            throw new Error(
                "Please log out and sign in again."
            );
        }


        const response =
            await fetch(

                API
                + "/hod-analytics/overview",

                {

                    headers: {

                        Authorization:
                            "Bearer "
                            + user.access_token

                    }

                }
            );


        if (!response.ok) {

            let detail =
                "HOD analytics could not be loaded.";


            try {

                const data =
                    await response.json();


                if (
                    typeof data.detail
                    === "string"
                ) {

                    detail =
                        data.detail;
                }

            } catch (error) {

                // Keep default message.
            }


            throw new Error(
                detail
            );
        }


        return response.json();
    }


    /* =========================================================
       RENDER TOP STATS
    ========================================================= */


    function renderStats(
        data
    ) {

        if (!hodDashboard) {

            return;
        }


        const values =
            hodDashboard.querySelectorAll(
                ".stats .stat-card h3"
            );


        const overview =
            data.overview
            ||
            data.summary
            ||
            data;


        if (values[0]) {

            values[0].textContent =
                overview.active_professors
                ??
                overview.total_professors
                ??
                data.active_professors
                ??
                0;
        }


        if (values[1]) {

            values[1].textContent =
                overview.total_student_problems
                ??
                overview.total_tickets
                ??
                data.total_student_problems
                ??
                data.total_tickets
                ??
                0;
        }


        if (values[2]) {

            values[2].textContent =
                overview.problems_resolved
                ??
                overview.resolved
                ??
                overview.resolved_tickets
                ??
                data.problems_resolved
                ??
                data.resolved
                ??
                0;
        }


        if (values[3]) {

            const average =
                overview.avg_resolution_minutes
                ??
                overview.average_resolution_minutes
                ??
                data.avg_resolution_minutes
                ??
                data.average_resolution_minutes;


            values[3].textContent =
                formatMinutes(
                    average
                );
        }
    }


    /* =========================================================
       FACULTY DETAILS
    ========================================================= */


    function getFacultyRows(
        data
    ) {

        const possible =
            data.faculty
            ??
            data.professors
            ??
            data.faculty_analytics
            ??
            data.analytics
            ??
            [];


        return Array.isArray(
            possible
        )
            ? possible
            : [];
    }


    function renderFaculty(
        data
    ) {

        const tbody =
            document.getElementById(
                "facultyAnalytics"
            );


        if (!tbody) {

            return;
        }


        const rows =
            getFacultyRows(
                data
            );


        tbody.innerHTML =
            "";


        if (!rows.length) {

            tbody.innerHTML = `

                <tr>

                    <td colspan="5">

                        <div class="empty-state">

                            <div class="icon">
                                📊
                            </div>

                            <h3>
                                No faculty analytics yet
                            </h3>

                            <p>
                                Faculty ticket activity
                                will appear here automatically.
                            </p>

                        </div>

                    </td>

                </tr>

            `;


            return;
        }


        rows.forEach(
            faculty => {

                const received =
                    faculty.problems_received
                    ??
                    faculty.received
                    ??
                    faculty.total_tickets
                    ??
                    faculty.ticket_count
                    ??
                    0;


                const resolved =
                    faculty.resolved
                    ??
                    faculty.resolved_count
                    ??
                    0;


                const pending =
                    faculty.pending
                    ??
                    faculty.pending_count
                    ??
                    Math.max(
                        Number(
                            received
                        )
                        -
                        Number(
                            resolved
                        ),
                        0
                    );


                const average =
                    faculty.avg_resolution_minutes
                    ??
                    faculty.average_resolution_minutes
                    ??
                    faculty.avg_minutes;


                const name =
                    faculty.name
                    ??
                    faculty.faculty_name
                    ??
                    faculty.full_name
                    ??
                    "Professor";


                const tr =
                    document.createElement(
                        "tr"
                    );


                tr.innerHTML = `

                    <td>
                        <strong>
                            ${escapeHtml(
                                name
                            )}
                        </strong>
                    </td>

                    <td>
                        ${escapeHtml(
                            received
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            resolved
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            pending
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            formatMinutes(
                                average
                            )
                        )}
                    </td>

                `;


                tbody.appendChild(
                    tr
                );


                renderSolvedProblems(
                    tbody,
                    faculty
                );


                renderResolutionPlot(
                    tbody,
                    faculty
                );
            }
        );
    }


    /* =========================================================
       SOLVED / RECEIVED PROBLEM DETAILS
    ========================================================= */


    function getProblems(
        faculty
    ) {

        const problems =
            faculty.questions
            ??
            faculty.tickets
            ??
            faculty.problems
            ??
            faculty.solved_questions
            ??
            [];


        return Array.isArray(
            problems
        )
            ? problems
            : [];
    }


    function renderSolvedProblems(
        tbody,
        faculty
    ) {

        const problems =
            getProblems(
                faculty
            );


        if (!problems.length) {

            return;
        }


        const detailRow =
            document.createElement(
                "tr"
            );


        const td =
            document.createElement(
                "td"
            );


        td.colSpan =
            5;


        td.style.background =
            "#fafbff";


        td.style.padding =
            "14px 18px";


        const title =
            document.createElement(
                "strong"
            );


        title.textContent =
            "Student problems handled";


        td.appendChild(
            title
        );


        problems.forEach(
            problem => {

                const box =
                    document.createElement(
                        "div"
                    );


                box.style.marginTop =
                    "10px";


                box.style.padding =
                    "10px 12px";


                box.style.border =
                    "1px solid #e5e7eb";


                box.style.borderRadius =
                    "8px";


                box.style.background =
                    "#ffffff";


                const topic =
                    problem.topic_title
                    ??
                    problem.topic
                    ??
                    "Topic";


                const student =
                    problem.student_name
                    ??
                    problem.student
                    ??
                    "Student";


                const status =
                    problem.status
                    ??
                    "pending";


                const question =
                    problem.doubt_text
                    ??
                    problem.question
                    ??
                    problem.problem
                    ??
                    "";


                box.innerHTML = `

                    <div>
                        <strong>
                            ${escapeHtml(
                                topic
                            )}
                        </strong>
                        ·
                        ${escapeHtml(
                            status
                        )}
                    </div>

                    <div style="
                        margin-top:4px;
                        color:#64748b;
                        font-size:11px;
                    ">
                        ${escapeHtml(
                            student
                        )}
                    </div>

                    <div style="
                        margin-top:6px;
                        white-space:pre-wrap;
                    ">
                        ${escapeHtml(
                            question
                        )}
                    </div>

                `;


                td.appendChild(
                    box
                );
            }
        );


        detailRow.appendChild(
            td
        );


        tbody.appendChild(
            detailRow
        );
    }


    /* =========================================================
       RESOLUTION TIME PLOT
    ========================================================= */


    function renderResolutionPlot(
        tbody,
        faculty
    ) {

        const plot =
            faculty.resolution_plot
            ??
            faculty.resolution_times
            ??
            [];


        if (
            !Array.isArray(
                plot
            )
            ||
            !plot.length
        ) {

            return;
        }


        const valid =
            plot
            .map(
                item => {

                    if (
                        typeof item
                        === "number"
                    ) {

                        return {

                            label:
                                "Resolved",

                            minutes:
                                item

                        };
                    }


                    return {

                        label:
                            item.topic_title
                            ??
                            item.topic
                            ??
                            item.label
                            ??
                            "Resolved",

                        minutes:
                            Number(
                                item.minutes
                                ??
                                item.resolution_minutes
                                ??
                                item.time_minutes
                                ??
                                0
                            )

                    };
                }
            )
            .filter(
                item =>
                    Number.isFinite(
                        item.minutes
                    )
                    &&
                    item.minutes >= 0
            );


        if (!valid.length) {

            return;
        }


        const maximum =
            Math.max(
                ...valid.map(
                    item =>
                        item.minutes
                ),
                1
            );


        const row =
            document.createElement(
                "tr"
            );


        const td =
            document.createElement(
                "td"
            );


        td.colSpan =
            5;


        td.style.padding =
            "14px 18px 18px";


        const heading =
            document.createElement(
                "strong"
            );


        heading.textContent =
            "Resolution time";


        td.appendChild(
            heading
        );


        valid.forEach(
            item => {

                const wrapper =
                    document.createElement(
                        "div"
                    );


                wrapper.style.marginTop =
                    "10px";


                const label =
                    document.createElement(
                        "div"
                    );


                label.style.fontSize =
                    "11px";


                label.style.marginBottom =
                    "4px";


                label.textContent =
                    (
                        item.label
                        +
                        " — "
                        +
                        formatMinutes(
                            item.minutes
                        )
                    );


                const track =
                    document.createElement(
                        "div"
                    );


                track.style.height =
                    "10px";


                track.style.borderRadius =
                    "999px";


                track.style.background =
                    "#ede9fe";


                const bar =
                    document.createElement(
                        "div"
                    );


                bar.style.height =
                    "100%";


                bar.style.borderRadius =
                    "999px";


                bar.style.background =
                    "linear-gradient(90deg,#6255e8,#8b5cf6)";


                bar.style.width =
                    Math.max(
                        4,
                        (
                            item.minutes
                            /
                            maximum
                        )
                        *
                        100
                    )
                    +
                    "%";


                track.appendChild(
                    bar
                );


                wrapper.append(
                    label,
                    track
                );


                td.appendChild(
                    wrapper
                );
            }
        );


        row.appendChild(
            td
        );


        tbody.appendChild(
            row
        );
    }


    /* =========================================================
       REFRESH
    ========================================================= */


    async function refresh() {

        try {

            const data =
                await loadOverview();


            renderStats(
                data
            );


            renderFaculty(
                data
            );


        } catch (error) {

            console.error(
                "HOD analytics error:",
                error
            );


            const tbody =
                document.getElementById(
                    "facultyAnalytics"
                );


            if (tbody) {

                tbody.innerHTML = `

                    <tr>

                        <td colspan="5">

                            <div class="empty-state">

                                <div class="icon">
                                    ⚠️
                                </div>

                                <h3>
                                    Analytics could not be loaded
                                </h3>

                                <p>
                                    ${escapeHtml(
                                        error.message
                                    )}
                                </p>

                            </div>

                        </td>

                    </tr>

                `;
            }
        }
    }


    /* =========================================================
       START
    ========================================================= */


    refresh();


    window.addEventListener(
        "focus",
        refresh
    );


    setInterval(
        refresh,
        10000
    );

})();