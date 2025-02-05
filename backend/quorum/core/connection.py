import uuid
from fastapi.websockets import WebSocketState
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[uuid.UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> uuid.UUID:
        await websocket.accept()
        client_id = uuid.uuid4()
        self.active_connections[client_id] = websocket
        return client_id

    async def disconnect(self, client_id: uuid.UUID, code: int):
        print(f"Disconnecting client: {client_id}")

        websocket = self.active_connections.pop(client_id)
        if websocket.client_state == WebSocketState.DISCONNECTED:
            print(f"WebSocket is already disconnected")
        else:
            print(f"Closing WebSocket")
            await websocket.close(code=code)

    async def broadcast(self, message: str, sender_id: uuid.UUID):
        disconnected_clients = []

        for client_id, websocket in self.active_connections.items():
            if client_id != sender_id:
                try:
                    await websocket.send_text(message)
                except Exception:
                    print(f"Error sending message to client {client_id}")
                    # If sending fails, mark client for removal
                    disconnected_clients.append(client_id)

        # Clean up any disconnected clients
        for client_id in disconnected_clients:
            print(f"Client {client_id} disconnected, removing from active connections")
            await self.disconnect(client_id)


manager = ConnectionManager()