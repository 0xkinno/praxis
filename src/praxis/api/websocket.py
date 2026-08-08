import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class PraxisProgressBroadcaster:
    """Manages active WebSocket connections for streaming pipeline execution progress."""
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total pool: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total pool: {len(self.active_connections)}")
            
    async def broadcast(self, message: dict):
        """Broadcasts a JSON payload to all connected clients."""
        for connection in self.active_connections[:]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send message to client, disconnecting: {e}")
                self.disconnect(connection)

broadcaster = PraxisProgressBroadcaster()
