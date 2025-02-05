from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from quorum.core.state import graph
from quorum.core.connection import manager

router = APIRouter(
    tags=["ws"], 
    prefix="/ws"
)


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
