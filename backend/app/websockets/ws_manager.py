import json
import logging
from typing import Dict, List, Set, Any
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Maps session_id -> Set of active WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Global connection set for system-wide dashboard telemetry listeners
        self.global_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, session_id: str = "global"):
        await websocket.accept()
        if session_id == "global":
            self.global_connections.add(websocket)
        else:
            if session_id not in self.active_connections:
                self.active_connections[session_id] = set()
            self.active_connections[session_id].add(websocket)
        logger.info(f"WebSocket client connected to topic '{session_id}'. Total global={len(self.global_connections)}, topic={len(self.active_connections.get(session_id, set()))}")
        try:
            from app.automation.safety_manager import safety_manager
            status_info = safety_manager.get_countdown_status(session_id if session_id != "global" else None)
            if status_info.get("active") or status_info.get("status") in ["COUNTDOWN", "INITIATING"]:
                await websocket.send_text(json.dumps({
                    "type": "AUTOMATION_COUNTDOWN",
                    "session_id": status_info.get("session_id"),
                    "action": "SHUTDOWN",
                    "remaining_sec": status_info.get("remaining_sec"),
                    "total_sec": status_info.get("total_sec"),
                    "status": status_info.get("status")
                }))
        except Exception as e:
            logger.debug(f"Could not send initial countdown state on connect: {e}")

    def disconnect(self, websocket: WebSocket, session_id: str = "global"):
        if session_id == "global":
            self.global_connections.discard(websocket)
        else:
            if session_id in self.active_connections:
                self.active_connections[session_id].discard(websocket)
                if not self.active_connections[session_id]:
                    del self.active_connections[session_id]
        logger.info(f"WebSocket client disconnected from topic '{session_id}'.")

    async def broadcast_to_session(self, session_id: str, message: Dict[str, Any]):
        """Pushes event message to all clients listening on session_id or global."""
        payload = json.dumps(message)
        
        target_sockets = set()
        if session_id in self.active_connections:
            target_sockets.update(self.active_connections[session_id])
        target_sockets.update(self.global_connections)

        stale_sockets = set()
        for connection in target_sockets:
            try:
                await connection.send_text(payload)
            except Exception as e:
                logger.warning(f"Failed to send message over WebSocket, marking as stale: {e}")
                stale_sockets.add(connection)

        # Cleanup stale connections
        for stale in stale_sockets:
            self.global_connections.discard(stale)
            if session_id in self.active_connections:
                self.active_connections[session_id].discard(stale)

    async def broadcast_global(self, message: Dict[str, Any]):
        """Pushes global metrics/telemetry to all connected clients."""
        payload = json.dumps(message)
        stale = set()
        for ws in self.global_connections:
            try:
                await ws.send_text(payload)
            except Exception:
                stale.add(ws)
        for s in stale:
            self.global_connections.discard(s)

ws_manager = ConnectionManager()
