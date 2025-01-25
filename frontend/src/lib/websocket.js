const BACKEND = "100.95.231.119:8000"
const BASE_ENDPOINT=`ws://${BACKEND}/api/v1/ws/`
const RPC_ENDPOINT=`ws://${BACKEND}/api/v1/ws/rpc`

let socket;

export function getWebSocket() {
  if (!socket) {
    console.log("Initialising websocket connection to backend.")
    socket = new WebSocket(BASE_ENDPOINT);

    socket.onopen = () => {
      console.log("WebSocket connection established.");
      socket.send("test")
    };

    socket.onmessage = (event) => {
      console.log("Message from server:", event.data);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = (event) => {
      console.log("WebSocket connection closed:", event.reason);
      // Optionally, you can handle reconnection logic here
    };

  }

  return socket;
}
