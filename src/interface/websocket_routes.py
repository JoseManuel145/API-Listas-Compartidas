from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from uuid import UUID
from src.Infrastructure.db.websocket_manager import ConnectionManager
from src.interface.dependencies import get_products_usecase

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/lists/{list_id}")
async def list_socket(websocket: WebSocket, list_id: UUID):
    await manager.connect(list_id, websocket)

    try:
        usecase = get_products_usecase()
        products = usecase.get_products_by_list(list_id)

        await websocket.send_json({
            "type": "INITIAL_STATE",
            "products": products
        })

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(list_id, websocket)