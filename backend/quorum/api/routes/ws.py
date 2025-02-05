import typing
import uuid
from fastapi.websockets import WebSocketState
from starlette import status
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from quorum.core.state import state

router = APIRouter(tags=["ws"], prefix="/ws")


class WSRoute:
    def __init__(self, websocket: WebSocket):
        self._websocket = websocket

    def __await__(self) -> typing.Generator:
        return self.dispatch().__await__()

    async def dispatch(self) -> None:
        """Websocket lifecycle.

        Raises:
            exc: _description_
        """
        # Websocket lifecycle
        await self.on_connect()

        close_code: int = status.WS_1000_NORMAL_CLOSURE
        try:
            while True:
                data = await self._websocket.receive_text()
                await self.on_receive(data)
        except WebSocketDisconnect:
            # Handle client normal disconnect here
            pass
        except Exception as exc:
            # Handle other types of errors here
            close_code = status.WS_1011_INTERNAL_ERROR
            raise exc from None
        finally:
            await self.on_disconnect(close_code)

    async def on_connect(self):
        # Handle your new connection here
        await self._websocket.accept()
        pass

    async def on_disconnect(self, close_code: int):
        # Handle client disconnect here
        pass

    async def on_receive(self, msg: typing.Any):
        # Handle client messaging here
        pass


class ConnectionManager:
    def __init__(self):
        # Store connections as a dict of client_id: WebSocket
        self.active_connections: dict[uuid.UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> uuid.UUID:
        await websocket.accept()
        client_id = uuid.uuid4()
        self.active_connections[client_id] = websocket
        return client_id

    async def disconnect(self, client_id: uuid.UUID, code: int):
        # Send the close message to the connected client
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
    state = graph.model_dump()
    try:
        payload = {"type": "state", "payload": state}
        await websocket.send_json(payload)

        while True:
            data = await websocket.receive_json()
            print("Received data:", data)

            method = data.get("method")
            match method:
                case "ping":
                    await websocket.send_json({"type": "pong"})
                case "echo":
                    await websocket.send_json({"type": "echo", "message": data.get("message")})
                case "addNode":
                    # TODO error handling
                    print("Received addNode RPC call")
                    x = data.get("payload").get("x")
                    y = data.get("payload").get("y")
                    print(f"Received x={x}, y={y}")
                    graph.add_node(x, y)
                    state = graph.model_dump()
                    payload = {"type": "state", "payload": state}
                    print("Sending state", state)
                    await websocket.send_json(payload)
                case _:
                    print(f"Unhandled method: {method}")
                    await websocket.send_json({"type": "error", "message": f"Method {method} not found"})

    except WebSocketDisconnect:
        print("Client disconnected websocket.")
    except Exception as exc:
        # Just during development, send the exception to the front end.
        await websocket.send_json({"type":"error", "message": str(exc)})
        print(f"{exc}")
    finally:
        # code 1011 chosen from https://www.rfc-editor.org/rfc/rfc6455.html#section-7.4.1
        await manager.disconnect(client_id, code=1011)
