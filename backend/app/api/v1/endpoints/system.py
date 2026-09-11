from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.monitoring.system_collector import SystemCollector
from app.websockets.ws_manager import ws_manager

router = APIRouter(tags=["System Metrics"])
collector = SystemCollector()

@router.get("/system/metrics")
async def get_system_metrics():
    return collector.collect()

@router.websocket("/ws/training")
async def websocket_global_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket, "global")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "global")
