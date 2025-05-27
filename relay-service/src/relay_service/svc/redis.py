import redis.asyncio as aioredis
from loguru import logger
from relay_service.config import settings
import json

REDIS_AGENT_PREFIX = "relay:agents:"


class RedisClient:
    def __init__(self, url: str):
        self.url = url
        self.redis = None

    async def connect(self):
        logger.info(f"Connecting to Redis at {self.url}")
        self.redis = aioredis.from_url(self.url, decode_responses=True)

    async def set_agent(self, agent_name: str, data: dict, ttl: int):
        key = REDIS_AGENT_PREFIX + agent_name.lower()
        await self.redis.set(key, json.dumps(data), ex=ttl)

    async def get_agents(self, filter_name: str = None):
        pattern = REDIS_AGENT_PREFIX + ("*" if not filter_name else filter_name.lower())
        keys = await self.redis.keys(pattern)
        res = []
        for key in keys:
            v = await self.redis.get(key)
            if v:
                res.append(json.loads(v))
        return res

    async def ping(self):
        await self.redis.ping()


async def get_redis():
    redis_client = RedisClient(settings.redis.url)
    if redis_client.redis is None:
        await redis_client.connect()
    return redis_client
