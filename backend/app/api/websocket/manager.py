from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Any
import json

ws_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        await ws.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(ws)

    def disconnect(self, room: str, ws: WebSocket):
        if room in self.active_connections:
            self.active_connections[room].remove(ws)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def broadcast(self, room: str, message: dict[str, Any]):
        if room not in self.active_connections:
            return
        data = json.dumps(message)
        for ws in self.active_connections[room]:
            try:
                await ws.send_text(data)
            except Exception:
                self.disconnect(room, ws)

    async def send_personal(self, ws: WebSocket, message: dict[str, Any]):
        await ws.send_text(json.dumps(message))


manager = ConnectionManager()


@ws_router.websocket("/ws/notifications")
async def notifications_ws(ws: WebSocket):
    await manager.connect("notifications", ws)
    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "ping":
                await manager.send_personal(ws, {"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect("notifications", ws)


@ws_router.websocket("/ws/chat/{room_id}")
async def chat_ws(ws: WebSocket, room_id: str):
    room = f"chat:{room_id}"
    await manager.connect(room, ws)
    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "message":
                await manager.broadcast(room, {
                    "type": "message",
                    "room_id": room_id,
                    "user_id": msg.get("user_id"),
                    "content": msg.get("content"),
                })
    except WebSocketDisconnect:
        manager.disconnect(room, ws)


@ws_router.websocket("/ws/market/{symbol}")
async def market_ws(ws: WebSocket, symbol: str):
    room = f"market:{symbol.upper()}"
    await manager.connect(room, ws)
    try:
        while True:
            data = await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(room, ws)


@ws_router.websocket("/ws/market")
async def market_all_ws(ws: WebSocket):
    room = "market:all"
    await manager.connect(room, ws)
    try:
        while True:
            data = await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(room, ws)
