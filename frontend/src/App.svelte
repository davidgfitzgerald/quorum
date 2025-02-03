<script>
	import Graph from './lib/components/Graph.svelte';
	import { getWebSocket } from './lib/websocket';

	/**
	 * On app startup connect to the backend.
	 */
	getWebSocket();
</script>

<h1>Quorum</h1>

<Graph></Graph>
