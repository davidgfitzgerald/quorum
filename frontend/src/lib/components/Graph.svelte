<script>
    import { onMount } from "svelte";
    import Graph from "graphology";

    // graphContainer is the div containing the graph
    let graphContainer;

    onMount(async () => {
        if (typeof window !== "undefined") {

            /**
             * Problem:
             * Importing Sigma at the top level gives the following error:
             * 
             * ReferenceError: WebGL2RenderingContext is not defined
             * 
             * Solution:
             * Dynamically import Sigma - this is because it depends on WebGL2RenderingContext
             * which is a browser-specific API (not available on the server).
             * 
             * There may be a better long term solution
             */
            const { Sigma } = await import("sigma");
            
            const graph = new Graph();
            graph.addNode("1", { label: "Node 1", x: 0, y: 0, size: 10, color: "blue" });
            graph.addNode("2", { label: "Node 2", x: 1, y: 1, size: 20, color: "red" });
            graph.addEdge("1", "2", { size: 5, color: "purple" });

            // Initialize Sigma with the graphology graph and container
            // Insert the graph in the graphContainer
            new Sigma(graph, graphContainer);
        }
    });
</script>

<h1>Quorum</h1>

<div bind:this={graphContainer} class="graph-container">
    <!-- Graph will be inserted here -->
</div>

<style>
    .graph-container {
        width: 100%; 
        height: 400px;
    }
</style>