
(function () {

    "use strict";


    function svgElement(
        name,
        attrs = {}
    ) {

        const element =
            document.createElementNS(
                "http://www.w3.org/2000/svg",
                name
            );


        Object.entries(
            attrs
        ).forEach(
            ([key, value]) => {

                element.setAttribute(
                    key,
                    String(value)
                );

            }
        );


        return element;
    }


    function text(
        svg,
        x,
        y,
        value,
        options = {}
    ) {

        const element =
            svgElement(
                "text",
                {
                    x,
                    y,

                    "text-anchor":
                        options.anchor
                        || "middle",

                    fill:
                        options.fill
                        || "#5d6578",

                    "font-size":
                        options.size
                        || 11,

                    "font-weight":
                        options.weight
                        || 700
                }
            );


        element.textContent =
            value;


        svg.appendChild(
            element
        );


        return element;
    }


    function line(
        svg,
        x1,
        y1,
        x2,
        y2,
        options = {}
    ) {

        const element =
            svgElement(
                "line",
                {
                    x1,
                    y1,
                    x2,
                    y2,

                    stroke:
                        options.stroke
                        || "#6d5dfc",

                    "stroke-width":
                        options.width
                        || 3,

                    "stroke-dasharray":
                        options.dash
                        || "",

                    "marker-end":
                        options.arrow
                        ? "url(#aiArrow)"
                        : ""
                }
            );


        svg.appendChild(
            element
        );


        return element;
    }


    function addArrowMarker(
        svg
    ) {

        const defs =
            svgElement(
                "defs"
            );


        const marker =
            svgElement(
                "marker",
                {
                    id: "aiArrow",
                    markerWidth: 10,
                    markerHeight: 10,
                    refX: 8,
                    refY: 3,
                    orient: "auto"
                }
            );


        const path =
            svgElement(
                "path",
                {
                    d:
                        "M0,0 L0,6 L9,3 z",

                    fill:
                        "#6d5dfc"
                }
            );


        marker.appendChild(
            path
        );


        defs.appendChild(
            marker
        );


        svg.appendChild(
            defs
        );
    }


    // ========================================================
    // LINE CHART
    // ========================================================

    function renderLineChart(
        spec
    ) {

        const svg =
            svgElement(
                "svg",
                {
                    viewBox:
                        "0 0 680 330"
                }
            );


        const points =
            Array.isArray(
                spec.points
            )
                ? spec.points
                : [];


        if (
            points.length < 2
        ) {

            text(
                svg,
                340,
                165,
                "Graph data unavailable"
            );

            return svg;
        }


        const left = 70;
        const right = 25;
        const top = 25;
        const bottom = 58;

        const graphWidth =
            680 - left - right;

        const graphHeight =
            330 - top - bottom;


        const xs =
            points.map(
                p => Number(p.x)
            );


        const ys =
            points.map(
                p => Number(p.y)
            );


        let minX =
            Math.min(
                0,
                ...xs
            );


        let maxX =
            Math.max(
                ...xs
            );


        let minY =
            Math.min(
                0,
                ...ys
            );


        let maxY =
            Math.max(
                ...ys
            );


        if (maxX === minX) {
            maxX += 1;
        }


        if (maxY === minY) {
            maxY += 1;
        }


        const sx =
            value =>
                left
                +
                (
                    (
                        value
                        - minX
                    )
                    /
                    (
                        maxX
                        - minX
                    )
                )
                *
                graphWidth;


        const sy =
            value =>
                top
                +
                graphHeight
                -
                (
                    (
                        value
                        - minY
                    )
                    /
                    (
                        maxY
                        - minY
                    )
                )
                *
                graphHeight;


        // grid

        for (
            let i = 0;
            i <= 5;
            i += 1
        ) {

            const gx =
                left
                +
                graphWidth
                *
                i
                /
                5;


            const gy =
                top
                +
                graphHeight
                *
                i
                /
                5;


            line(
                svg,
                gx,
                top,
                gx,
                top + graphHeight,
                {
                    stroke: "#efedf7",
                    width: 1
                }
            );


            line(
                svg,
                left,
                gy,
                left + graphWidth,
                gy,
                {
                    stroke: "#efedf7",
                    width: 1
                }
            );
        }


        // axes

        line(
            svg,
            left,
            top + graphHeight,
            left + graphWidth,
            top + graphHeight,
            {
                stroke: "#697082",
                width: 1.5
            }
        );


        line(
            svg,
            left,
            top,
            left,
            top + graphHeight,
            {
                stroke: "#697082",
                width: 1.5
            }
        );


        // curve

        const polyline =
            svgElement(
                "polyline",
                {
                    points:
                        points
                            .map(
                                p =>
                                    `${sx(Number(p.x))},${sy(Number(p.y))}`
                            )
                            .join(" "),

                    fill: "none",

                    stroke: "#6d5dfc",

                    "stroke-width": 3,

                    "stroke-linejoin":
                        "round",

                    "stroke-linecap":
                        "round"
                }
            );


        svg.appendChild(
            polyline
        );


        points.forEach(
            p => {

                svg.appendChild(
                    svgElement(
                        "circle",
                        {
                            cx:
                                sx(
                                    Number(p.x)
                                ),

                            cy:
                                sy(
                                    Number(p.y)
                                ),

                            r: 4,

                            fill:
                                "#ffffff",

                            stroke:
                                "#6d5dfc",

                            "stroke-width":
                                2.5
                        }
                    )
                );

            }
        );


        text(
            svg,
            left + graphWidth / 2,
            318,
            spec.x_label || "x",
            {
                size: 11,
                weight: 800
            }
        );


        const ylabel =
            text(
                svg,
                18,
                top + graphHeight / 2,
                spec.y_label || "y",
                {
                    size: 11,
                    weight: 800
                }
            );


        ylabel.setAttribute(
            "transform",
            `rotate(-90 18 ${top + graphHeight / 2})`
        );


        return svg;
    }


    // ========================================================
    // REFLECTION
    // ========================================================

    function reflectionDiagram() {

        const svg =
            svgElement(
                "svg",
                {
                    viewBox:
                        "0 0 680 330"
                }
            );


        addArrowMarker(
            svg
        );


        line(
            svg,
            70,
            215,
            610,
            215,
            {
                stroke: "#4f5566",
                width: 4
            }
        );


        line(
            svg,
            340,
            42,
            340,
            300,
            {
                stroke: "#a5a9b4",
                width: 2,
                dash: "7 7"
            }
        );


        line(
            svg,
            120,
            70,
            340,
            215,
            {
                arrow: true
            }
        );


        line(
            svg,
            340,
            215,
            560,
            70,
            {
                arrow: true
            }
        );


        text(
            svg,
            205,
            105,
            "Incident ray"
        );


        text(
            svg,
            475,
            105,
            "Reflected ray"
        );


        text(
            svg,
            370,
            55,
            "Normal",
            {
                anchor: "start",
                size: 10
            }
        );


        text(
            svg,
            340,
            242,
            "Mirror",
            {
                fill: "#4f5566"
            }
        );


        return svg;
    }


    // ========================================================
    // REFRACTION
    // ========================================================

    function refractionDiagram() {

        const svg =
            svgElement(
                "svg",
                {
                    viewBox:
                        "0 0 680 330"
                }
            );


        addArrowMarker(
            svg
        );


        svg.appendChild(
            svgElement(
                "rect",
                {
                    x: 0,
                    y: 180,
                    width: 680,
                    height: 150,
                    fill: "#eef8ff"
                }
            )
        );


        line(
            svg,
            60,
            180,
            620,
            180,
            {
                stroke: "#6b7280",
                width: 2
            }
        );


        line(
            svg,
            340,
            35,
            340,
            305,
            {
                stroke: "#a5a9b4",
                width: 2,
                dash: "7 7"
            }
        );


        line(
            svg,
            120,
            55,
            340,
            180,
            {
                arrow: true
            }
        );


        line(
            svg,
            340,
            180,
            455,
            305,
            {
                arrow: true
            }
        );


        text(
            svg,
            95,
            45,
            "Air",
            {
                anchor: "start"
            }
        );


        text(
            svg,
            95,
            207,
            "Glass / water",
            {
                anchor: "start",
                fill: "#4080a8"
            }
        );


        text(
            svg,
            230,
            95,
            "Incident ray"
        );


        text(
            svg,
            455,
            270,
            "Refracted ray"
        );


        return svg;
    }


    // ========================================================
    // CONVEX LENS
    // ========================================================

    function convexLensDiagram() {

        const svg =
            svgElement(
                "svg",
                {
                    viewBox:
                        "0 0 680 330"
                }
            );


        addArrowMarker(
            svg
        );


        line(
            svg,
            40,
            190,
            640,
            190,
            {
                stroke: "#a6abb8",
                width: 1.5,
                dash: "6 6"
            }
        );


        const lens =
            svgElement(
                "path",
                {
                    d:
                        "M340 50 C295 115 295 265 340 325 C385 265 385 115 340 50 Z",

                    fill:
                        "#eef1ff",

                    stroke:
                        "#6d5dfc",

                    "stroke-width":
                        2.5
                }
            );


        svg.appendChild(
            lens
        );


        line(
            svg,
            120,
            190,
            120,
            90,
            {
                arrow: true
            }
        );


        text(
            svg,
            120,
            74,
            "Object"
        );


        line(
            svg,
            120,
            90,
            340,
            90
        );


        line(
            svg,
            340,
            90,
            555,
            190,
            {
                arrow: true
            }
        );


        line(
            svg,
            120,
            90,
            340,
            190,
            {
                stroke: "#9b8cf7"
            }
        );


        line(
            svg,
            340,
            190,
            565,
            285,
            {
                stroke: "#9b8cf7",
                arrow: true
            }
        );


        text(
            svg,
            340,
            38,
            "Convex lens"
        );


        return svg;
    }


    // ========================================================
    // GENERIC PHYSICS DIAGRAM
    // ========================================================

    function genericDiagram(
        spec
    ) {

        const svg =
            svgElement(
                "svg",
                {
                    viewBox:
                        "0 0 680 330"
                }
            );


        addArrowMarker(
            svg
        );


        const box =
            (
                x,
                y,
                width,
                height,
                label
            ) => {

                svg.appendChild(
                    svgElement(
                        "rect",
                        {
                            x,
                            y,
                            width,
                            height,

                            rx: 12,

                            fill:
                                "#f5f2ff",

                            stroke:
                                "#cec7ff",

                            "stroke-width":
                                2
                        }
                    )
                );


                text(
                    svg,
                    x + width / 2,
                    y + height / 2 + 4,
                    label,
                    {
                        size: 11
                    }
                );
            };


        if (
            spec.diagram ===
            "newton_forces"
        ) {

            box(
                270,
                125,
                140,
                85,
                "Object"
            );


            line(
                svg,
                410,
                168,
                575,
                168,
                {
                    arrow: true
                }
            );


            line(
                svg,
                270,
                190,
                115,
                190,
                {
                    arrow: true,
                    stroke: "#9b8cf7"
                }
            );


            line(
                svg,
                340,
                125,
                340,
                50,
                {
                    arrow: true
                }
            );


            line(
                svg,
                340,
                210,
                340,
                300,
                {
                    arrow: true,
                    stroke: "#9b8cf7"
                }
            );


            text(
                svg,
                505,
                150,
                "Applied force"
            );


            text(
                svg,
                180,
                215,
                "Friction"
            );


            text(
                svg,
                375,
                65,
                "Normal",
                {
                    anchor: "start"
                }
            );


            text(
                svg,
                375,
                290,
                "Weight",
                {
                    anchor: "start"
                }
            );


            return svg;
        }


        box(
            80,
            125,
            150,
            75,
            "Input"
        );


        box(
            265,
            125,
            150,
            75,
            "Physics"
        );


        box(
            450,
            125,
            150,
            75,
            "Result"
        );


        line(
            svg,
            230,
            162,
            260,
            162,
            {
                arrow: true
            }
        );


        line(
            svg,
            415,
            162,
            445,
            162,
            {
                arrow: true
            }
        );


        return svg;
    }


    function renderDiagram(
        spec
    ) {

        if (
            spec.diagram ===
            "reflection"
        ) {

            return reflectionDiagram();
        }


        if (
            spec.diagram ===
            "refraction"
        ) {

            return refractionDiagram();
        }


        if (
            spec.diagram ===
            "convex_lens"
        ) {

            return convexLensDiagram();
        }


        return genericDiagram(
            spec
        );
    }


    // ========================================================
    // PUBLIC RENDER FUNCTION
    // ========================================================

    window.renderTutorVisuals =
        function (
            afterRow,
            visuals
        ) {

            if (
                !afterRow
                ||
                !Array.isArray(
                    visuals
                )
                ||
                visuals.length === 0
            ) {

                return;
            }


            let anchor =
                afterRow;


            visuals.forEach(
                spec => {

                    const row =
                        document.createElement(
                            "div"
                        );


                    row.className =
                        "ai-tutor-visual-row";


                    const card =
                        document.createElement(
                            "div"
                        );


                    card.className =
                        "ai-tutor-visual-card";


                    const header =
                        document.createElement(
                            "div"
                        );


                    header.className =
                        "ai-tutor-visual-header";


                    const title =
                        document.createElement(
                            "div"
                        );


                    title.className =
                        "ai-tutor-visual-title";


                    title.textContent =
                        spec.title
                        || "Physics visual";


                    const badge =
                        document.createElement(
                            "div"
                        );


                    badge.className =
                        "ai-tutor-visual-badge";


                    badge.textContent =
                        spec.kind ===
                        "line_chart"
                            ? "Graph"
                            : "Diagram";


                    header.append(
                        title,
                        badge
                    );


                    const stage =
                        document.createElement(
                            "div"
                        );


                    stage.className =
                        "ai-tutor-visual-stage";


                    if (
                        spec.kind ===
                        "line_chart"
                    ) {

                        stage.appendChild(
                            renderLineChart(
                                spec
                            )
                        );

                    } else {

                        stage.appendChild(
                            renderDiagram(
                                spec
                            )
                        );
                    }


                    const caption =
                        document.createElement(
                            "div"
                        );


                    caption.className =
                        "ai-tutor-visual-caption";


                    caption.textContent =
                        spec.caption
                        || "";


                    card.append(
                        header,
                        stage,
                        caption
                    );


                    row.appendChild(
                        card
                    );


                    anchor.insertAdjacentElement(
                        "afterend",
                        row
                    );


                    anchor =
                        row;

                }
            );


            const container =
                document.getElementById(
                    "embeddedAiMessages"
                );


            if (container) {

                container.scrollTop =
                    container.scrollHeight;
            }
        };

})();
