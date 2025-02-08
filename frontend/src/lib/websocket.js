/**
 * This file contains a singleton client-side WebSocket
 * that connects to the backend.
 */
import { graphData, web } from './state.svelte';

const BACKEND = '127.0.0.1:8000'; // TODO: make configurable
const RPC_ENDPOINT = `ws://${BACKEND}/api/v1/ws/rpc`;

/**
 * Connect to the backend and return the singleton websocket.
 * @returns {WebSocket}
 */
export function getWebSocket() {
	if (web.socket !== null) return web.socket;

	console.log('Initialising WebSocket connection to backend');
	web.socket = new WebSocket(RPC_ENDPOINT);

	web.socket.onopen = () => {
		console.log('WebSocket connection to backend established');
	};

	web.socket.onmessage = (event) => {
		console.debug('Message from backend:', event.data);
		const jsonData = JSON.parse(event.data);

		if (jsonData.type === undefined) {
			console.error("Cannot parse message: expected a 'type' field")
			return 
		}

		const type = jsonData.type

		switch (type) {
			case "state":
				graphData.state = jsonData.payload;
				return 
			case "pong":
				console.log("Received pong from backend")
				break;
			case "error":
				console.error("Backend error:")
				console.error(jsonData.error)
				break
			default:
				console.warn(`Unhandled type=${type} message`);
				break;
		}
	};

	web.socket.onerror = (error) => {
		console.error('WebSocket error:', error);
	};

	web.socket.onclose = (event) => {
		console.log('WebSocket connection to backend closed/failed:', event.reason);
		web.socket = null;
		
		console.log("Trying to reconnect websocket")
		getWebSocket()
	};
}
