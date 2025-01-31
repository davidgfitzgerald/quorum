<script>
	import Graph from "./lib/components/Graph.svelte";
	import { connectBackend } from "./lib/websocket";

	/**
	 * On app startup connect to the backend.
	 */ 
	connectBackend()
</script>

<h1>Quorum</h1>

<Graph></Graph>