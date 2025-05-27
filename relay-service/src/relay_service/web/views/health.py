from fastapi import APIRouter, Depends
from loguru import logger
from relay_service.svc.redis import get_redis
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/healthz", tags=["Health"])


@router.get("")
async def healthz(redis=Depends(get_redis)):
    try:
        await redis.ping()
    except Exception as e:
        logger.exception("Redis health check failed")
        return JSONResponse(
            status_code=503, content={"status": "unhealthy", "error": str(e)}
        )
    return {"status": "ok", "relay_peer_id": None}
