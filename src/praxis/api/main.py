import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from ..config import settings
from ..db.database import init_db
from .websocket import broadcaster
from .routes import (
    health,
    catalog,
    assessments,
    assets,
    domains,
    contracts,
    ml,
    propagation,
    digests
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes external system connections and SQLite tables during startup."""
    logger.info(f"Starting PRAXIS API in {settings.mode} mode.")
    if settings.mode == "live":
        try:
            await init_db()
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")
    yield
    logger.info("PRAXIS API shutting down.")

app = FastAPI(
    title="PRAXIS API",
    description="Data Trust Intelligence Engine backend services.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes under /api
app.include_router(health.router, prefix="/api")
app.include_router(catalog.router, prefix="/api")
app.include_router(assessments.router, prefix="/api")
app.include_router(assets.router, prefix="/api")
app.include_router(domains.router, prefix="/api")
app.include_router(contracts.router, prefix="/api")
app.include_router(ml.router, prefix="/api")
app.include_router(propagation.router, prefix="/api")
app.include_router(digests.router, prefix="/api")

@app.websocket("/ws/assessment")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection route for streaming pipeline progress events."""
    await broadcaster.connect(websocket)
    try:
        while True:
            # Keep connection open by listening for any ping message (optional)
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket ping text: {data}")
    except WebSocketDisconnect:
        broadcaster.disconnect(websocket)
    except Exception as e:
        logger.warning(f"WebSocket execution error: {e}")
        broadcaster.disconnect(websocket)
