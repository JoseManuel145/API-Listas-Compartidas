from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends 
from uuid import UUID
from src.Infrastructure.db.websocket_manager import manager
from src.interface.dependencies import get_products_usecase

router = APIRouter()

@router.websocket("/ws/lists/{list_id}")
async def list_socket(
    websocket: WebSocket, 
    list_id: UUID, 
    usecase = Depends(get_products_usecase) 
):
    await manager.connect(list_id, websocket)

    try:
     
        products = usecase.get_products_by_list(list_id)

        
        products_dict = [
            {"id": str(p.id), "name": p.name, "quantity": p.quantity, "status": p.status} 
            for p in products
        ]

        await websocket.send_json({
            "type": "INITIAL_STATE",
            "products": products_dict
        })

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(list_id, websocket)