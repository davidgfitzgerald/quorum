<script>
    import Graph from "graphology";

    // graphContainer is the div containing the graph
    let graphContainer;
    const g = new Graph()
    let graph = $state(new Graph());

    // $inspect(graph)
    
    let graphJSON = $derived(JSON.stringify(graph.export(), null, 2))

    function refreshState() {
        /**
         * Problem:
         * Svelte is not picking up that the graph object has changed 
         * with addNode and addEdge calls.
         * 
         * Solution:
         * Re-assign graph to tell svelte that the state has changed
         * and to re-render the element in the UI.
         * 
         * TODO:
         * Better long term solution
         */
        const graphTmp = graph;
        graph = null
        graph = graphTmp
    }

    $effect(async () => {
        if (typeof window !== "undefined") {

            /**
             * Problem:
             * Importing Sigma at the top level gives the following error:
             * 
             * ReferenceError: WebGL2RenderingContext is not defined
             * 
             * Temporary Solution:
             * Dynamically import Sigma - this is because it depends on WebGL2RenderingContext
             * which is a browser-specific API (not available on the server).
             * 
             * TODO:
             * Better long term solution
             */
            const { Sigma } = await import("sigma");
            
            console.log("Graph state updated")
            graph.addNode("1", { label: "Node 1", x: 0, y: 0, size: 10, color: "blue" });
            graph.addNode("2", { label: "Node 2", x: 1, y: 1, size: 20, color: "red" });
            graph.addEdge("1", "2", { size: 5, color: "purple" });

            refreshState()  // TODO remove need for this call

            // Initialize Sigma with the graphology graph and container
            // Insert the graph in the graphContainer
            new Sigma(graph, graphContainer);
        }
    });
</script>

<h1 class="text-4xl p-8">Quorum</h1>

<div 
    bind:this={graphContainer}
    class="graph-container"
>
    <!-- Graph will be inserted here -->
</div>

<h1 class="text-4xl p-8">Graph JSON</h1>

<div class="p-8">
    <pre>{graphJSON}</pre>
</div>

<style>
    .graph-container {
        width: 100%; 
        height: 400px;
    }
</style>