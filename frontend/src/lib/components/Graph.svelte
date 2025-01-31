<script>
    import Graph from "graphology";
    import Sigma from "sigma";
	import { data } from "../state.svelte";
    
    // The div containing the sigma graph
    let sigmaGraphContainer
    
    // The sigma graph instance.
    let sigmaGraph = null;
    
    /**
     * The reactive graphology graph data derived whenever the
     * graph state changes.
     */
    let graph = $derived(new Graph().import(data.state))

    $effect(() => {
        /**
         * This effect runs whenever reactive dependencies 
         * change. In this case, this is whenever `graph` 
         * changes.
         * 
         * Initialise the sigma instance if it does not yet 
         * exist. Else update the sigma instance with the
         * new `graph`.
         *
         * This is somewhat of a workaround. It would be nicer
         * if we didn't use `$effect` here and instead used 
         * `$derived`.
        */
        if (sigmaGraph) {
            sigmaGraph.setGraph(graph)
        } else {
            sigmaGraph = new Sigma(graph, sigmaGraphContainer)
        }
    })
</script>

<h1>Graph</h1>

<div bind:this={sigmaGraphContainer} class="graph-container">
    <!-- Sigma graph will be inserted here -->
</div>

<style>
    .graph-container {
        width: 100%;
        height: 700px;
    }
</style>