/**
 * This file contains a singleton client-side WebSocket
 * that connects to the backend.
 */
import { graphState } from "./state.svelte.js";


const BACKEND = "100.95.231.119:8000"
// const BASE_ENDPOINT=`ws://${BACKEND}/api/v1/ws/`
const RPC_ENDPOINT=`ws://${BACKEND}/api/v1/ws/rpc`

let socket;


export function getWebSocket() {
  if (!socket) {
    console.log("Initialising websocket connection to backend.")
    socket = new WebSocket(RPC_ENDPOINT);

    socket.onopen = () => {
      console.log("WebSocket connection established.");
    };

    socket.onmessage = (event) => {
        console.log("Message from backend:", event.data);
        if (event.data.type == "state") {
            graphState = event.data.payload
        }
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = (event) => {
      console.log("WebSocket connection to backend closed/failed:", event.reason);
      // Optionally, you can handle reconnection logic here
    };

  }

  return socket;
}
