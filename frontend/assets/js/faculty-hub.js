(function () {

    'use strict';


    // ============================================================
    // CONFIG
    // ============================================================

    const API =
        'http://127.0.0.1:8000';


    let user = null;


    try {

        user = JSON.parse(
            localStorage.getItem(
                'myCampusUser'
            ) || 'null'
        );

    } catch (error) {

        user = null;
    }


    if (!user) {

        return;
    }


    // ============================================================
    // COMMON HELPERS
    // ============================================================

    const el = (
        tag,
        text,
        cls
    ) => {

        const element =
            document.createElement(
                tag
            );


        if (
            text !== undefined
        ) {

            element.textContent =
                text;
        }


        if (cls) {

            element.className =
                cls;
        }


        return element;
    };


    async function request(
        path,
        options = {}
    ) {

        if (
            !user.access_token
        ) {

            throw new Error(
                'Please log out and sign in again to activate resources and faculty replies.'
            );
        }


        const headers = {

            ...options.headers,

            Authorization:
                'Bearer '
                + user.access_token
        };


        const response =
            await fetch(

                API
                + '/faculty-hub'
                + path,

                {
                    ...options,
                    headers
                }
            );


        if (
            !response.ok
        ) {

            const data =
                await response
                    .json()
                    .catch(
                        () => ({})
                    );


            throw new Error(

                typeof data.detail ===
                'string'

                    ? data.detail

                    : 'Request could not be completed.'
            );
        }


        return response;
    }


    async function json(
        path,
        options
    ) {

        return (
            await request(
                path,
                options
            )
        ).json();
    }


    function action(
        text,
        fn
    ) {

        const button =
            el(
                'button',
                text,
                'hub-button'
            );


        button.type =
            'button';


        button.onclick =
            fn;


        return button;
    }


    // ============================================================
    // FACULTY RESOURCE CARD
    // ============================================================

    function resourceCard(
        item
    ) {

        const card =
            el(
                'article',
                undefined,
                'hub-item'
            );


        card.append(

            el(
                'strong',
                item.title
            ),

            el(
                'p',
                (
                    item.topic_title
                    + ' - '
                    + item.resource_type
                    + ' - '
                    + item.faculty_name
                )
            )
        );


        if (
            item.description
        ) {

            card.append(
                el(
                    'p',
                    item.description
                )
            );
        }


        if (
            item.is_file
        ) {

            const status =
                el(
                    'span',
                    undefined,
                    'hub-status'
                );


            card.append(

                action(
                    'Download file',

                    async event => {

                        const button =
                            event.currentTarget;


                        button.disabled =
                            true;


                        try {

                            const response =
                                await request(

                                    '/resources/'
                                    + item.id
                                    + '/download'
                                );


                            const blob =
                                await response.blob();


                            const objectUrl =
                                URL.createObjectURL(
                                    blob
                                );


                            const anchor =
                                el(
                                    'a'
                                );


                            const disposition =
                                response.headers.get(
                                    'content-disposition'
                                ) || '';


                            const extensionMatch =
                                disposition.match(
                                    /filename="[^"]*(\.[a-z0-9]+)"/i
                                );


                            anchor.href =
                                objectUrl;


                            anchor.download =
                                (
                                    'resource-'
                                    + item.id
                                    + (
                                        extensionMatch
                                            ? extensionMatch[1]
                                            : ''
                                    )
                                );


                            document.body.append(
                                anchor
                            );


                            anchor.click();


                            anchor.remove();


                            setTimeout(
                                () => {

                                    URL.revokeObjectURL(
                                        objectUrl
                                    );

                                },
                                10000
                            );


                            status.textContent =
                                'Downloaded.';


                        } catch (error) {

                            status.textContent =
                                error.message;


                        } finally {

                            button.disabled =
                                false;
                        }
                    }
                ),

                status
            );


        } else {

            try {

                const resourceUrl =
                    new URL(
                        item.url
                    );


                if (
                    [
                        'http:',
                        'https:'
                    ].includes(
                        resourceUrl.protocol
                    )
                ) {

                    const anchor =
                        el(
                            'a',
                            'Open resource',
                            'hub-button'
                        );


                    anchor.href =
                        resourceUrl.href;


                    anchor.target =
                        '_blank';


                    anchor.rel =
                        'noopener noreferrer';


                    card.append(
                        anchor
                    );
                }

            } catch (error) {

                // Invalid URL.
            }
        }


        return card;
    }


    function showResources(
        host,
        items
    ) {

        host.replaceChildren();


        if (
            !items.length
        ) {

            host.append(
                el(
                    'p',
                    'No faculty resources have been shared here yet.'
                )
            );


            return;
        }


        items.forEach(
            resource => {

                host.append(
                    resourceCard(
                        resource
                    )
                );
            }
        );
    }


    // ============================================================
    // FACULTY / STUDENT TICKETS
    // ============================================================

    async function renderTickets(
        host,
        facultyView
    ) {

        const data =
            await json(
                '/tickets'
            );


        const tickets =
            Array.isArray(
                data.tickets
            )
                ? data.tickets
                : [];


        host.replaceChildren();


        if (
            !tickets.length
        ) {

            host.append(

                el(
                    'p',

                    facultyView

                        ? 'No student doubts yet.'

                        : 'Your submitted doubts and faculty replies will appear here.'
                )
            );
        }


        for (
            const ticket
            of tickets
        ) {

            const card =
                el(
                    'article',
                    undefined,
                    'hub-item'
                );


            const topicTitle =
                ticket.topic?.title
                || 'Topic';


            const ticketStatus =
                String(
                    ticket.status
                    || 'new'
                )
                .replaceAll(
                    '_',
                    ' '
                );


            const secondLine =
                facultyView

                    ? (
                        (
                            ticket.student?.name
                            || 'Student'
                        )
                        + ' - '
                        + (
                            ticket.subject?.name
                            || 'Subject'
                        )
                    )

                    : (
                        'Faculty: '
                        + (
                            ticket.assigned_faculty?.name
                            || 'Awaiting assignment'
                        )
                    );


            card.append(

                el(
                    'strong',
                    topicTitle
                    + ' - '
                    + ticketStatus
                ),

                el(
                    'p',
                    secondLine
                ),

                el(
                    'p',
                    ticket.doubt_text
                    || '',
                    'hub-prewrap'
                )
            );


            if (
                ticket.faculty_response
            ) {

                card.append(

                    el(
                        'strong',
                        'Faculty reply'
                    ),

                    el(
                        'p',
                        ticket.faculty_response,
                        'hub-prewrap'
                    )
                );


            } else if (
                facultyView
            ) {

                const status =
                    el(
                        'p',
                        undefined,
                        'hub-status'
                    );


                if (
                    ticket.status ===
                    'new'
                ) {

                    card.append(

                        action(
                            'Take this doubt',

                            async event => {

                                const button =
                                    event.currentTarget;


                                button.disabled =
                                    true;


                                try {

                                    await json(

                                        '/tickets/'
                                        + ticket.id
                                        + '/start',

                                        {
                                            method:
                                                'PATCH'
                                        }
                                    );


                                    await renderTickets(
                                        host,
                                        true
                                    );


                                } catch (error) {

                                    status.textContent =
                                        error.message;


                                    button.disabled =
                                        false;
                                }
                            }
                        )
                    );
                }


                const label =
                    el(
                        'label',
                        'Your reply'
                    );


                const reply =
                    el(
                        'textarea'
                    );


                reply.id =
                    'hub-reply-'
                    + ticket.id;


                label.htmlFor =
                    reply.id;


                reply.rows =
                    4;


                reply.maxLength =
                    5000;


                reply.placeholder =
                    'Explain the concept and steps the student should try.';


                const send =
                    action(

                        'Send reply & resolve',

                        async () => {

                            const replyText =
                                reply.value
                                    .trim();


                            if (
                                replyText.length <
                                3
                            ) {

                                status.textContent =
                                    'Please write a helpful reply.';


                                return;
                            }


                            send.disabled =
                                true;


                            try {

                                await json(

                                    '/tickets/'
                                    + ticket.id
                                    + '/resolve',

                                    {
                                        method:
                                            'PATCH',

                                        headers: {
                                            'Content-Type':
                                                'application/json'
                                        },

                                        body:
                                            JSON.stringify({
                                                faculty_response:
                                                    replyText
                                            })
                                    }
                                );


                                await renderTickets(
                                    host,
                                    true
                                );


                            } catch (error) {

                                status.textContent =
                                    error.message;


                                send.disabled =
                                    false;
                            }
                        }
                    );


                card.append(
                    label,
                    reply,
                    send,
                    status
                );
            }


            host.append(
                card
            );
        }


        if (
            facultyView
        ) {

            const counters = [

                [
                    'newTickets',
                    'new'
                ],

                [
                    'progressTickets',
                    'in_progress'
                ],

                [
                    'resolvedTickets',
                    'resolved'
                ]
            ];


            for (
                const [
                    elementId,
                    statusName
                ]
                of counters
            ) {

                const element =
                    document.getElementById(
                        elementId
                    );


                if (element) {

                    element.textContent =
                        tickets.filter(
                            ticket =>
                                ticket.status
                                === statusName
                        ).length;
                }
            }
        }
    }


    // ============================================================
    // FACULTY PORTAL
    // ============================================================

    if (
        user.role ===
        'faculty'
    ) {

        const form =
            document.querySelector(
                'form[onsubmit="demoUpload(event)"]'
            );


        if (!form) {

            return;
        }


        form.removeAttribute(
            'onsubmit'
        );


        form.classList.add(
            'hub-form'
        );


        form.innerHTML = `
            <div class="field">
                <label for="hub-subject">
                    Subject
                </label>

                <select
                    id="hub-subject"
                    required
                ></select>
            </div>


            <div class="field">
                <label for="hub-topic">
                    Topic
                </label>

                <select
                    id="hub-topic"
                    name="topic_id"
                    required
                ></select>
            </div>


            <div class="field">
                <label for="hub-title">
                    Resource title
                </label>

                <input
                    id="hub-title"
                    name="title"
                    required
                    maxlength="200"
                    placeholder="Example: Newton's laws worked problems"
                >
            </div>


            <div class="field">
                <label for="hub-type">
                    Resource type
                </label>

                <select
                    id="hub-type"
                    name="resource_type"
                >
                    <option value="notes">
                        Notes / document
                    </option>

                    <option value="video">
                        Video
                    </option>

                    <option value="visualization">
                        Interactive model
                    </option>

                    <option value="game">
                        Game / activity
                    </option>
                </select>
            </div>


            <div class="field">
                <label for="hub-file">
                    Upload a file
                    (maximum 25 MB)
                </label>

                <input
                    id="hub-file"
                    name="file"
                    type="file"
                    accept=".pdf,.txt,.png,.jpg,.jpeg,.mp4,.webm,.pptx,.docx"
                >

                <small>
                    PDF, TXT, images, video,
                    PowerPoint or Word.
                    Or paste a link below.
                </small>
            </div>


            <div class="field">
                <label for="hub-url">
                    Resource link
                    (instead of a file)
                </label>

                <input
                    id="hub-url"
                    name="url"
                    type="url"
                    placeholder="https://..."
                >
            </div>


            <div class="field">
                <label for="hub-description">
                    Description
                </label>

                <textarea
                    id="hub-description"
                    name="description"
                    maxlength="5000"
                    rows="3"
                ></textarea>
            </div>


            <button
                class="primary-btn"
                type="submit"
            >
                Share with students
            </button>


            <p
                id="hub-upload-status"
                role="status"
            ></p>


            <h3>
                My shared resources
            </h3>


            <div
                id="hub-resource-list"
            ></div>
        `;


        const msg =
            form.querySelector(
                '#hub-upload-status'
            );


        const mine =
            form.querySelector(
                '#hub-resource-list'
            );


        const subjects =
            form.querySelector(
                '#hub-subject'
            );


        const topics =
            form.querySelector(
                '#hub-topic'
            );


        let catalog = {
            subjects: [],
            topics: []
        };


        function fillTopics() {

            topics.replaceChildren(

                new Option(
                    'Select topic',
                    ''
                )
            );


            catalog.topics
                .filter(
                    topic =>
                        topic.subject_id ===
                        Number(
                            subjects.value
                        )
                )
                .forEach(
                    topic => {

                        topics.add(

                            new Option(
                                topic.title,
                                topic.id
                            )
                        );
                    }
                );
        }


        subjects.onchange =
            fillTopics;


        async function refreshMine() {

            const data =
                await json(
                    '/resources/mine'
                );


            showResources(
                mine,
                data.resources || []
            );


            const resourceCount =
                document.getElementById(
                    'resourceCount'
                );


            if (
                resourceCount
            ) {

                resourceCount.textContent =
                    (
                        data.resources
                        || []
                    ).length;
            }
        }


        form.onsubmit =
            async event => {

                event.preventDefault();


                const file =
                    form.querySelector(
                        '#hub-file'
                    ).files[0];


                const url =
                    form.querySelector(
                        '#hub-url'
                    ).value.trim();


                if (
                    Boolean(file)
                    ===
                    Boolean(url)
                ) {

                    msg.textContent =
                        'Select one file OR enter one link.';


                    return;
                }


                if (
                    file
                    &&
                    file.size >
                    (
                        25
                        * 1024
                        * 1024
                    )
                ) {

                    msg.textContent =
                        'File must be 25 MB or smaller.';


                    return;
                }


                const button =
                    form.querySelector(
                        'button[type=submit]'
                    );


                button.disabled =
                    true;


                msg.textContent =
                    'Sharing resource...';


                try {

                    const body =
                        new FormData(
                            form
                        );


                    if (!file) {

                        body.delete(
                            'file'
                        );
                    }


                    await json(
                        '/resources',
                        {
                            method:
                                'POST',

                            body
                        }
                    );


                    form.querySelector(
                        '#hub-title'
                    ).value = '';


                    form.querySelector(
                        '#hub-file'
                    ).value = '';


                    form.querySelector(
                        '#hub-url'
                    ).value = '';


                    form.querySelector(
                        '#hub-description'
                    ).value = '';


                    msg.textContent =
                        (
                            'Shared successfully. '
                            + 'Students can find it under '
                            + 'this topic\'s Faculty Resources button.'
                        );


                    await refreshMine();


                } catch (error) {

                    msg.textContent =
                        error.message;


                } finally {

                    button.disabled =
                        false;
                }
            };


        const ticketHost =
            document.getElementById(
                'ticketContainer'
            );


        if (ticketHost) {

            const refreshButton =
                action(

                    'Refresh student doubts',

                    () => {

                        renderTickets(
                            ticketHost,
                            true
                        )
                        .catch(
                            error => {

                                ticketHost.textContent =
                                    error.message;
                            }
                        );
                    }
                );


            ticketHost.before(
                refreshButton
            );
        }


        const professorDashboard =
            document.getElementById(
                'professorDashboard'
            );


        if (
            professorDashboard
        ) {

            professorDashboard.style.display =
                'block';
        }


        const navigationTargets = [

            [
                'resourceNav',
                form
            ],

            [
                'ticketsNav',
                ticketHost
            ]
        ];


        for (
            const [
                id,
                target
            ]
            of navigationTargets
        ) {

            const nav =
                document.getElementById(
                    id
                );


            if (
                !nav
                ||
                !target
            ) {

                continue;
            }


            nav.style.display =
                '';


            nav.onclick =
                () => {

                    target.scrollIntoView({
                        behavior:
                            'smooth'
                    });
                };


            nav.tabIndex =
                0;


            nav.onkeydown =
                event => {

                    if (
                        event.key ===
                        'Enter'
                    ) {

                        nav.click();
                    }
                };
        }


        (
            async () => {

                try {

                    catalog =
                        await json(
                            '/catalog'
                        );


                    subjects.add(

                        new Option(
                            'Select subject',
                            ''
                        )
                    );


                    (
                        catalog.subjects
                        || []
                    ).forEach(
                        subject => {

                            subjects.add(

                                new Option(
                                    subject.name,
                                    subject.id
                                )
                            );
                        }
                    );


                    fillTopics();


                    await refreshMine();


                    if (
                        ticketHost
                    ) {

                        await renderTickets(
                            ticketHost,
                            true
                        );
                    }


                } catch (error) {

                    msg.textContent =
                        error.message;


                    if (
                        ticketHost
                    ) {

                        ticketHost.textContent =
                            error.message;
                    }
                }
            }
        )();


        return;
    }


    // ============================================================
    // STUDENT PORTAL
    // ============================================================

    if (
        user.role !==
        'student'
    ) {

        return;
    }


    const main =
        document.querySelector(
            'main'
        );


    if (!main) {

        return;
    }


    // ============================================================
    // STUDENT FACULTY REPLIES PANEL
    // ============================================================

    const panel =
        el(
            'section',
            undefined,
            'hub-panel'
        );


    panel.append(
        el(
            'h2',
            'My faculty replies'
        )
    );


    const ticketHost =
        el(
            'div'
        );


    const ticketStatus =
        el(
            'p',
            undefined,
            'hub-status'
        );


    async function refreshStudentTickets() {

        try {

            await renderTickets(
                ticketHost,
                false
            );


            ticketStatus.textContent =
                '';


        } catch (error) {

            ticketStatus.textContent =
                error.message;
        }
    }


    panel.append(

        action(
            'Refresh replies',
            refreshStudentTickets
        ),

        ticketStatus,

        ticketHost
    );


    main.append(
        panel
    );


    refreshStudentTickets();


    // ============================================================
    // FACULTY RESOURCE DIALOG
    // ============================================================

    const resourceDialog =
        el(
            'dialog',
            undefined,
            'hub-dialog'
        );


    const resourceHeading =
        el(
            'h2'
        );


    const resourceList =
        el(
            'div'
        );


    resourceDialog.append(

        resourceHeading,

        action(
            'Close',
            () =>
                resourceDialog.close()
        ),

        resourceList
    );


    document.body.append(
        resourceDialog
    );


    window.openFacultyResources =
        async (
            topicId,
            title
        ) => {

            resourceHeading.textContent =
                (
                    'Faculty Resources - '
                    + title
                );


            resourceList.textContent =
                'Loading...';


            if (
                !resourceDialog.open
            ) {

                resourceDialog.showModal();
            }


            try {

                const data =
                    await json(

                        '/resources/topic/'
                        + topicId
                    );


                showResources(
                    resourceList,
                    data.resources || []
                );


            } catch (error) {

                resourceList.textContent =
                    error.message;
            }
        };


    // ============================================================
    // AI -> FACULTY HANDOFF STATE
    // ============================================================

    let activeFacultyTopic =
        null;


    let activeFacultyAiAttempted =
        false;


    let handoffRequestNumber =
        0;


    // ============================================================
    // READ AI TUTOR CONVERSATION FROM CURRENT PAGE
    // ============================================================

    function getCurrentAiTutorTopicId() {

        const topicNumber =
            document.getElementById(
                'embeddedAiTopicNumber'
            );


        if (!topicNumber) {

            return null;
        }


        const text =
            String(
                topicNumber.textContent
                || ''
            );


        const match =
            text.match(
                /\d+/
            );


        if (!match) {

            return null;
        }


        return Number(
            match[0]
        );
    }


    function collectAiTutorHistory(
        topic
    ) {

        const currentAiTopicId =
            getCurrentAiTutorTopicId();


        /*
            Do not use stale AI conversation
            from another topic.
        */

        if (
            currentAiTopicId
            &&
            Number(
                topic.id
            )
            !==
            currentAiTopicId
        ) {

            return [];
        }


        const rows =
            Array.from(

                document.querySelectorAll(
                    '#embeddedAiMessages .embedded-ai-row'
                )
            );


        const history = [];


        let studentHasSpoken =
            false;


        for (
            const row
            of rows
        ) {

            const bubble =
                row.querySelector(
                    '.embedded-ai-bubble'
                );


            if (!bubble) {

                continue;
            }


            const text =
                String(
                    bubble.textContent
                    || ''
                ).trim();


            if (!text) {

                continue;
            }


            if (
                row.classList.contains(
                    'user'
                )
            ) {

                studentHasSpoken =
                    true;


                history.push({

                    role:
                        'user',

                    content:
                        text
                });


                continue;
            }


            if (
                row.classList.contains(
                    'tutor'
                )
            ) {

                /*
                    Skip the automatic opening greeting.
                    Only AI explanations after the student's
                    first real message are useful to faculty.
                */

                if (
                    !studentHasSpoken
                ) {

                    continue;
                }


                history.push({

                    role:
                        'assistant',

                    content:
                        text
                });
            }
        }


        return history.slice(
            -12
        );
    }


    // ============================================================
    // SAFE LOCAL HANDOFF IF NETWORK FAILS
    // ============================================================

    function buildEmergencyHandoff(
        topic,
        history
    ) {

        const studentMessages =
            history.filter(
                item =>
                    item.role ===
                    'user'
            );


        const latestStudentMessage =
            studentMessages.length

                ? studentMessages[
                    studentMessages.length
                    - 1
                ].content

                : 'The student is requesting additional explanation.';


        return (
            'Student is requesting faculty support for "'
            + (
                topic.title
                || 'this topic'
            )
            + '". '
            + 'The latest difficulty expressed was: "'
            + latestStudentMessage
            + '". '
            + (
                history.length

                    ? (
                        'The student has already discussed this topic '
                        + 'with the AI Tutor. Please use a different '
                        + 'teaching approach rather than repeating '
                        + 'the same explanation.'
                    )

                    : (
                        'No usable AI Tutor conversation was available '
                        + 'for the automatic handoff.'
                    )
            )
        );
    }


    // ============================================================
    // OPEN FACULTY MODAL + AUTO GENERATE DESCRIPTION
    // ============================================================

    window.openFacultyModal =
        async function (
            topic
        ) {

            activeFacultyTopic =
                topic;


            activeFacultyAiAttempted =
                false;


            const thisRequest =
                ++handoffRequestNumber;


            const modal =
                document.getElementById(
                    'facultyModal'
                );


            const modalTopic =
                document.getElementById(
                    'modalTopic'
                );


            const doubtBox =
                document.getElementById(
                    'doubtText'
                );


            const sendButton =
                document.getElementById(
                    'sendDoubtBtn'
                );


            if (
                !modal
                ||
                !modalTopic
                ||
                !doubtBox
                ||
                !sendButton
            ) {

                alert(
                    'Faculty support window is unavailable.'
                );


                return;
            }


            modalTopic.textContent =
                topic.title
                || 'Current Topic';


            modal.classList.add(
                'active'
            );


            doubtBox.value =
                'AI is preparing a summary for your faculty...';


            doubtBox.disabled =
                true;


            sendButton.disabled =
                true;


            sendButton.textContent =
                'Preparing AI handoff...';


            const history =
                collectAiTutorHistory(
                    topic
                );


            try {

                const data =
                    await json(

                        '/doubts/handoff',

                        {
                            method:
                                'POST',

                            headers: {
                                'Content-Type':
                                    'application/json'
                            },

                            body:
                                JSON.stringify({

                                    topic_id:
                                        Number(
                                            topic.id
                                        ),

                                    history:
                                        history
                                })
                        }
                    );


                /*
                    Modal may have been closed
                    while AI was generating.
                */

                if (
                    thisRequest
                    !==
                    handoffRequestNumber
                ) {

                    return;
                }


                if (
                    !activeFacultyTopic
                    ||
                    Number(
                        activeFacultyTopic.id
                    )
                    !==
                    Number(
                        topic.id
                    )
                ) {

                    return;
                }


                const summary =
                    String(
                        data.summary
                        || ''
                    ).trim();


                if (!summary) {

                    throw new Error(
                        'AI handoff summary was empty.'
                    );
                }


                doubtBox.value =
                    summary;


                activeFacultyAiAttempted =
                    Boolean(
                        data.ai_attempted
                    );


            } catch (error) {

                console.error(
                    'Faculty handoff generation failed:',
                    error
                );


                if (
                    thisRequest
                    !==
                    handoffRequestNumber
                ) {

                    return;
                }


                doubtBox.value =
                    buildEmergencyHandoff(
                        topic,
                        history
                    );


                activeFacultyAiAttempted =
                    history.length > 0;


            } finally {

                if (
                    thisRequest
                    !==
                    handoffRequestNumber
                ) {

                    return;
                }


                doubtBox.disabled =
                    false;


                sendButton.disabled =
                    false;


                sendButton.textContent =
                    'Send to Faculty';


                doubtBox.focus();


                doubtBox.setSelectionRange(
                    doubtBox.value.length,
                    doubtBox.value.length
                );
            }
        };


    // ============================================================
    // CLOSE FACULTY MODAL
    // ============================================================

    window.closeFacultyModal =
        function () {

            handoffRequestNumber++;


            const modal =
                document.getElementById(
                    'facultyModal'
                );


            if (modal) {

                modal.classList.remove(
                    'active'
                );
            }


            const doubtBox =
                document.getElementById(
                    'doubtText'
                );


            if (doubtBox) {

                doubtBox.disabled =
                    false;
            }


            const sendButton =
                document.getElementById(
                    'sendDoubtBtn'
                );


            if (sendButton) {

                sendButton.disabled =
                    false;


                sendButton.textContent =
                    'Send to Faculty';
            }


            activeFacultyTopic =
                null;


            activeFacultyAiAttempted =
                false;
        };


    // ============================================================
    // FACULTY MODAL BACKDROP
    // ============================================================

    window.modalBackdropClick =
        function (
            event
        ) {

            if (
                event.target.id ===
                'facultyModal'
            ) {

                window.closeFacultyModal();
            }
        };


    // ============================================================
    // SUBMIT AI-GENERATED HANDOFF TO FACULTY
    // ============================================================

    window.submitDoubt =
        async function () {

            if (
                !activeFacultyTopic
            ) {

                return;
            }


            const doubtBox =
                document.getElementById(
                    'doubtText'
                );


            const sendButton =
                document.getElementById(
                    'sendDoubtBtn'
                );


            if (
                !doubtBox
                ||
                !sendButton
            ) {

                return;
            }


            const text =
                doubtBox.value
                    .trim();


            if (
                text.length <
                3
            ) {

                alert(
                    'Please wait for the AI summary or enter a faculty handoff description.'
                );


                return;
            }


            sendButton.disabled =
                true;


            sendButton.textContent =
                'Sending...';


            try {

                await json(

                    '/doubts',

                    {
                        method:
                            'POST',

                        headers: {
                            'Content-Type':
                                'application/json'
                        },

                        body:
                            JSON.stringify({

                                topic_id:
                                    Number(
                                        activeFacultyTopic.id
                                    ),

                                doubt_text:
                                    text,

                                ai_attempted:
                                    activeFacultyAiAttempted
                            })
                    }
                );


                alert(
                    'Your doubt has been sent to faculty.'
                );


                window.closeFacultyModal();


                window.dispatchEvent(

                    new Event(
                        'faculty-doubt-sent'
                    )
                );


            } catch (error) {

                alert(
                    error.message
                );


            } finally {

                sendButton.disabled =
                    false;


                sendButton.textContent =
                    'Send to Faculty';
            }
        };


    // ============================================================
    // STUDENT EVENT REFRESH
    // ============================================================

    window.addEventListener(
        'faculty-doubt-sent',
        refreshStudentTickets
    );


    window.addEventListener(
        'focus',
        refreshStudentTickets
    );


})();