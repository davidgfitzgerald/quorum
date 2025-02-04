<script>
	import Graph from 'graphology';
	import Sigma from 'sigma';
	import { data } from '../state.svelte';
	import { getWebSocket } from '../websocket';

	// The clients websocket connection to the backend
	const socket = getWebSocket()

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
	let graph = $derived(new Graph().import(data.state));

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
			sigmaInstance = new Sigma(graph, sigmaGraphContainer);
		}
	});

	/**
	 * @param {MouseEvent} event
	 */
	function addNode(event) {
		if (socket.readyState === WebSocket.CLOSED) {
			console.error("Cannot send addNode request: Backend connection has closed/failed.")
			return
		}
		
		const {x, y} = getGridCoords(event)
		socket.send(JSON.stringify({"method": "addNode", "payload": {x, y}}))
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
		width: 100%;
		height: 700px;
		outline: medium solid lightgrey;
	}
</style>
