from fastapi import APIRouter, Query, Depends, status
from relay_service.models.peers import AgentRegisterRequest, AgentInfo
from relay_service.svc.redis import get_redis
from relay_service.config import settings

router = APIRouter(prefix="/peers", tags=["Peers"])


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register_agent(payload: AgentRegisterRequest, redis=Depends(get_redis)):
    agent = AgentInfo(
        agent_name=payload.agent_name, peer_id=payload.peer_id, addresses=payload.addrs
    )
    await redis.set_agent(
        payload.agent_name, agent.model_dump(), ttl=settings.redis.ttl_secs
    )
    return


@router.get("", response_model=list[AgentInfo])
async def get_peers(agent_name: str | None = Query(None), redis=Depends(get_redis)):
    return await redis.get_agents(filter_name=agent_name)
