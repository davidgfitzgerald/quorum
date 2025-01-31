/**
 * This file contains a singleton client-side WebSocket
 * that connects to the backend.
 */
const BACKEND = "127.0.0.1:8000"  // TODO: make configurable
const RPC_ENDPOINT = `ws://${BACKEND}/api/v1/ws/rpc`

let socket = null;


export function connectBackend() {
    /**
     * Connect to the backend and return the singleton websocket.
     */
    if (socket) return socket

    console.log("Initialising WebSocket connection to backend")
    socket = new WebSocket(RPC_ENDPOINT)

    socket.onopen = () => {
        console.log("WebSocket connection to backend established")
    }

    socket.onmessage = (event) => {
        console.log("Message from backend:", event.data)
    }

    socket.onerror = (error) => {
        console.error('WebSocket error:', error)
    }

    socket.onclose = (event) => {
        console.log("WebSocket connection to backend closed/failed:", event.reason)
        socket = null;
    }
}