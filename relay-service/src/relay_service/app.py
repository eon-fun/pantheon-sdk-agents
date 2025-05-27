from contextlib import asynccontextmanager

from relay_service.config import settings
from fastapi import FastAPI
from loguru import logger
from relay_service.web.views.peers import router as peers_router
from relay_service.web.views.health import router as health_router
from relay_service.svc.relay import start_relay


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=settings.log_level)
    relay_peer_id = await start_relay()
    app.state.relay_peer_id = relay_peer_id
    yield


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Startup and shutdown event lifecycle handler."""

#     logger.info("[startup] Starting Relay Service...")
#     logger.info("Relay Service started successfully!")
#     yield
#     logger.info("[shutdown] Shutting down relay-service...")


def get_app() -> FastAPI:
    """Initialize FastAPI app with lifespan event handling."""
    _app = FastAPI(
        title=settings.SERVICE_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    _app.include_router(peers_router)
    _app.include_router(health_router)
    return _app


app = get_app()
