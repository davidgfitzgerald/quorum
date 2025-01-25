from pathlib import Path
import json
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["ws"], prefix="/ws")

# This is a json representation of a graph in a format usable by sigma.js
# It exists in lieu of a database
STATE = Path(__file__).parent.parent.parent / "core" / "state.json"


class ConnectionManager:
    def __init__(self):
        # Store connections as a dict of client_id: WebSocket
        self.active_connections: dict[uuid.UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> uuid.UUID:
        await websocket.accept()
        client_id = uuid.uuid4()
        self.active_connections[client_id] = websocket
        return client_id

    async def disconnect(self, client_id: uuid.UUID):
        self.active_connections.pop(client_id)

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


@router.websocket("/")
async def websocket_echo(websocket: WebSocket):
    client_id = await manager.connect(websocket)

    try:
        await websocket.send_json({"client_id": str(client_id)})
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", client_id)
    except WebSocketDisconnect:
        await manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat", client_id)


@router.websocket("/rpc")
async def websocket_rpc(websocket: WebSocket):
    client_id = await manager.connect(websocket)
    try:
        # Immediately return the client_id to the client
        # await websocket.send_json({"client_id": str(client_id)})
        payload = {"type": "state", "payload": json.load(STATE.open())}
        await websocket.send_json(payload)

        while True:
            data = await websocket.receive_json()

            method = data.get("method")
            match method:
                case "ping":
                    await websocket.send_json({"pong": True})
                case "echo":
                    await websocket.send_json({"echo": data.get("message")})
                case "addNode":
                    payload = {"type": "state", "payload": json.load(STATE.open())}
                    await websocket.send_json(payload)
                case _:
                    await websocket.send_json({"error": f"Method {method} not found"})

    except WebSocketDisconnect:
        await manager.disconnect(client_id)
    except Exception as exc:
        print(f"{exc}")
        # await manager.disconnect(client_id)
