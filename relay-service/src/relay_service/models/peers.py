from pydantic import BaseModel, Field, constr


class AgentRegisterRequest(BaseModel):
    agent_name: constr(strip_whitespace=True, min_length=3, max_length=128)
    peer_id: constr(strip_whitespace=True, min_length=10, max_length=64)
    addrs: list[str] = Field(..., min_length=1)


class AgentInfo(BaseModel):
    agent_name: str
    peer_id: str
    addresses: list[str]
