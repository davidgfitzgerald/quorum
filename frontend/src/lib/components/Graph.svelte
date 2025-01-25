<script>
	import { createCounter } from '$lib/utils/Counter.svelte.js';
	import Graph from 'graphology';
	import { getWebSocket } from '$lib/websocket.js';
	import { graphState } from '$lib/state.svelte.js';

	const socket = getWebSocket();

	let graphContainer; // The div containing the graph

	let graph = $derived(new Graph().import(graphState.state));

	let nodeCounter = createCounter();

	function addNode() {
		socket.send(
			JSON.stringify({
				method: 'addNode',
				payload: { label: `Node ${nodeCounter.count}`, x: 3, y: 2, size: 30, color: 'green' }
			})
		);
	}

	$effect(async () => {
		if (typeof window !== 'undefined') {
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
			const { Sigma } = await import('sigma');

			// Initialize Sigma with the graphology graph and container
			// Insert the graph in the graphContainer
			new Sigma(graph, graphContainer);
		}
	});
</script>

<h1 class="p-8 text-4xl">Quorum</h1>

<!-- TODO: handle a11y properly -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div bind:this={graphContainer} onclick={addNode} class="graph-container">
	<!-- Graph will be inserted here -->
</div>

<h1 class="p-8 text-4xl">Backend State</h1>

<div class="p-8">
	<pre>{JSON.stringify(graphState, null, 2)}</pre>
</div>

<style>
	.graph-container {
		width: 100%;
		height: 400px;
	}
</style>
