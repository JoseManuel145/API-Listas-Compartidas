from fastapi import WebSocket
from typing import Dict, List
from uuid import UUID

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, List[WebSocket]] = {}

    async def connect(self, list_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(list_id, []).append(websocket)

    def disconnect(self, list_id: UUID, websocket: WebSocket):
        self.active_connections[list_id].remove(websocket)

    async def broadcast(self, list_id: UUID, message: dict):
        for connection in self.active_connections.get(list_id, []):
            await connection.send_json(message)

manager = ConnectionManager()