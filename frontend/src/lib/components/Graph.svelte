<script>
	import { createCounter } from "$lib/utils/Counter.svelte.js";
    import Graph from "graphology";
    import { getWebSocket } from "$lib/websocket.js"

    
    const socket = getWebSocket();

    // graphContainer is the div containing the graph
    let graphContainer;
    let graph = $state(new Graph());

    let nodeCounter = createCounter()
    
    // TODO - get state from server
    let graphJSON = $derived(JSON.stringify(graph.export(), null, 2))

    function addNode() {
        // Server call
        graph.addNode(nodeCounter.next(), { label: `Node ${nodeCounter.count}`, x: 3, y: 2, size: 30, color: "green" });
    }

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
            graph.addNode(nodeCounter.next(), { label: `Node ${nodeCounter.count}`, x: 0, y: 0, size: 10, color: "blue" });
            graph.addNode(nodeCounter.next(), { label: `Node ${nodeCounter.count}`, x: 1, y: 1, size: 20, color: "red" });
            graph.addEdge(1, "2", { size: 5, color: "purple" });

            refreshState()  // TODO remove need for this call

            // Initialize Sigma with the graphology graph and container
            // Insert the graph in the graphContainer
            new Sigma(graph, graphContainer);
        }
    });
</script>

<h1 class="text-4xl p-8">Quorum</h1>

<!-- TODO: handle a11y properly -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div 
    bind:this={graphContainer}
    onclick={addNode}
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