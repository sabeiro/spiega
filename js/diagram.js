(function() {
    let svg, g, simulation;
    let tooltip = document.getElementById('tooltip');
    let width = 800, height = 600;

    function initGraph() {
        const container = document.getElementById('graph');
        width = container.clientWidth;
        height = container.clientHeight;

        svg = d3.select("#graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .style("font", "12px sans-serif");

        g = svg.append("g");

        simulation = d3.forceSimulation()
                   .force("link", d3.forceLink().id(d => d.id).distance(100))
                   .force("charge", d3.forceManyBody().strength(-300))
                   .force("x", d3.forceX(width / 2))
                   .force("y", d3.forceY(height / 2));

        // Create link group
        const linkGroup = g.append("g")
                           .attr("class", "links")
                           .attr("id", "link-group");

        // Create node group
        const nodeGroup = g.append("g")
                           .attr("class", "nodes")
                           .attr("id", "node-group");

        // Define link line template
        const link = linkGroup.append("line")
                              .attr("class", "link")
                              .attr("stroke", "rgba(255, 255, 255, 0.3)")
                              .attr("stroke-width", 2);

        // Define node group template
        const node = nodeGroup.append("g")
                              .attr("class", "node")
                              .attr("id", "node-group");

        // Setup tick event handler
        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("transform", d => `translate(${d.x},${d.y})`);
        });

        // Expose groups and simulation for loadFile to use
        window.graphLinkGroup = linkGroup;
        window.graphNodeGroup = nodeGroup;
        window.graphSimulation = simulation;

        // Attach event listeners AFTER svg is created
        svg.on('mousemove', function(event, d) {
            if (d) showTooltip(event, d);
        });

        svg.on('mouseleave', hideTooltip);

        window.addEventListener('resize', function() {
            width = document.getElementById('graph').clientWidth;
            height = document.getElementById('graph').clientHeight;
            svg.attr("viewBox", [0, 0, width, height]);
        });
    }

    function loadFile(file) {
        const reader = new FileReader();
        const status = document.getElementById('status');

        reader.onload = function(e) {
            try {
                const data = JSON.parse(e.target.result);
                status.textContent = "✅ File loaded successfully!";
                status.className = "status success";

                const nodesData = data.nodes || [];
                const linksData = data.links || [];

                // Clear existing data
                window.graphLinkGroup.selectAll("line").remove();
                window.graphNodeGroup.selectAll("g").remove();

                // Create links
                const linkSelection = window.graphLinkGroup.selectAll("line")
                                       .data(linksData);

                linkSelection.enter().append("line")
                             .attr("class", "link");

                linkSelection.exit().remove();

                // Create nodes
                const nodeSelection = window.graphNodeGroup.selectAll("g")
                                       .data(nodesData);

                nodeSelection.enter().append("g")
                             .attr("class", "node")
                             .call(d3.drag()
                                .on("start", dragstarted)
                                .on("drag", dragged)
                                .on("end", dragended));

                nodeSelection.append("circle")
                             .attr("r", d => calculateRadius(d.duty, d.duty_range))
                             .attr("fill", d => d.color)
                             .attr("stroke", "white")
                             .attr("stroke-width", 2);

                nodeSelection.append("text")
                             .attr("dy", 4)
                             .attr("text-anchor", "middle")
                             .text(d => d.id);

                // Update existing nodes
                nodeSelection.merge(nodeSelection.enter())
                             .attr("transform", d => `translate(${d.x},${d.y})`);

                // Update simulation
                window.graphSimulation.nodes(nodesData);
                window.graphSimulation.force("link").links(linksData);
                window.graphSimulation.force("charge").strength(nodesData.length * -50);
                window.graphSimulation.force("x").strength(0.1);
                window.graphSimulation.force("y").strength(0.1);

                window.graphSimulation.alpha(1).restart();

                tooltip.style.opacity = 0;

            } catch (error) {
                status.textContent = "❌ Error loading file: " + error.message;
                status.className = "status error";
            }
        };

        reader.readAsText(file);
    }

    function calculateRadius(duty, duty_range) {
        if (!duty_range || duty_range.length < 2) return 15;
        const min = duty_range[0];
        const max = duty_range[1];
        const range = max - min;
        const normalized = (duty - min) / range;
        return 15 - (normalized * 10);
    }

    function dragstarted(event, d) {
        if (!event.active) window.graphSimulation.alphaTarget(0).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) window.graphSimulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    function showTooltip(event, d) {
        const description = d.description || "No description available";
        tooltip.innerHTML = `<strong>${d.id}</strong><br/>${description}`;
        tooltip.style.left = (event.pageX + 15) + "px";
        tooltip.style.top = (event.pageY - 15) + "px";
        tooltip.classList.add('visible');
    }

    function hideTooltip() {
        tooltip.classList.remove('visible');
    }

    document.getElementById('file-input').addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            loadFile(e.target.files[0]);
        }
    });

    initGraph();
})();
