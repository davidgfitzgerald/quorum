/**
 * This file contains a singleton client-side WebSocket
 * that connects to the backend.
 */
import { data } from './state.svelte';
import { websocketState } from './ws.svelte';

const BACKEND = '127.0.0.1:8000'; // TODO: make configurable
const RPC_ENDPOINT = `ws://${BACKEND}/api/v1/ws/rpc`;
// let socket = null;

/**
 * Connect to the backend and return the singleton websocket.
 * @returns {WebSocket}
 */
export function getWebSocket() {
	if (websocketState.websocket !== null) return websocketState.websocket;

	console.log('Initialising WebSocket connection to backend');
	websocketState.websocket = new WebSocket(RPC_ENDPOINT);

	websocketState.websocket.onopen = () => {
		console.log('WebSocket connection to backend established');
	};

	websocketState.websocket.onmessage = (event) => {
		console.debug('Message from backend:', event.data);
		const jsonData = JSON.parse(event.data);

		if (jsonData.type === undefined) {
			console.error("Cannot parse message: expected a 'type' field")
			return 
		}

		const type = jsonData.type

		switch (type) {
			case "state":
				data.state = jsonData.payload;
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

	websocketState.websocket.onerror = (error) => {
		console.error('WebSocket error:', error);
	};

	websocketState.websocket.onclose = (event) => {
		console.log('WebSocket connection to backend closed/failed:', event.reason);
		websocketState.websocket = null;
		
		console.log("Trying to reconnect websocket")
		getWebSocket()
	};
}
