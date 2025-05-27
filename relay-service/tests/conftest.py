import pytest
from unittest.mock import AsyncMock
from relay_service.app import app
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def mocked_redis():
    """An async mock for your RedisClient."""
    mock = AsyncMock()
    mock.set_agent.return_value = None
    mock.get_agents.return_value = []
    mock.ping.return_value = True
    return mock


@pytest.fixture(autouse=True)
def override_redis_dependency(mocked_redis):
    """Override FastAPI's get_redis dependency with the mock for all tests."""
    from relay_service.svc.redis import get_redis

    async def _override():
        return mocked_redis

    app.dependency_overrides[get_redis] = _override
    yield
    app.dependency_overrides.pop(get_redis, None)


@pytest.fixture
async def client():
    """Create a FastAPI test client using HTTPX (ASGITransport)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
