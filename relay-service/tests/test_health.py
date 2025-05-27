import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestHealth:
    endpoint = "/healthz"

    async def test_get_health(
        self,
        client: AsyncClient,
    ):
        get_response = await client.get(
            self.endpoint,
        )

        assert get_response.status_code == 200
