<script>
	import Graph from 'graphology';
	import Sigma from 'sigma';
	import { graphData, web } from '../state.svelte';

	// The reactive websocket connected to the backend
	const websocket = $derived(web.socket)

	// The div containing the sigma graph
	let sigmaGraphContainer;

	// The sigma graph instance.
	/**
	 * @type {Sigma}
	 */
	let sigmaInstance = null;

	/**
	 * The reactive graphology graph data derived whenever the
	 * graph state changes.
	 */
	let graph = $derived(new Graph().import(graphData.state));

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
		if (sigmaInstance) {
			sigmaInstance.setGraph(graph);
		} else {
			sigmaInstance = new Sigma(
				graph, 
				sigmaGraphContainer,
				{
					renderEdgeLabels: true,
				}
			);
		}
	});

	/**
	 * @param {MouseEvent} event
	 */
	function addNode(event) {
		if (websocket.readyState === WebSocket.CLOSED) {
			console.error("Cannot send addNode request: Backend connection has closed/failed.")
			return
		}
		
		const {x, y} = getGridCoords(event)
		websocket.send(JSON.stringify({"method": "addNode", "payload": {x, y}}))
	}

	/**
	 * Find the coordinates on the sigma grid.
	 * 
	 * Converts the mouse viewport co-ordinates into sigma
	 * graph co-ordinates.
	 * @param {MouseEvent} event
	 * @returns {import('sigma/types').Coordinates} format: {x: ..., y: ...}
	*/
	function getGridCoords(event) {
		return sigmaInstance.viewportToGraph({ x: event.offsetX, y: event.offsetY})
	}
</script>

<h1>Graph</h1>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_mouse_events_have_key_events -->
<div
	bind:this={sigmaGraphContainer}
	class="graph-container"
	onclick={addNode}
	>
	<!-- Sigma graph will be inserted here -->
</div>

<style>
	.graph-container {
		width: 98%;
		margin-left: 1%;
		margin-right: 1%;

		height: 700px;
		outline: medium solid lightgrey;
	}
</style>
