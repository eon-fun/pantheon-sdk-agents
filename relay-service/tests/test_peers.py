import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestPeers:
    endpoint = "/peers"

    async def test_get_all_peers(self, client: AsyncClient):
        get_response = await client.get(
            self.endpoint,
        )

        assert get_response.status_code == 200

    async def test_register_and_get_peers(self, client: AsyncClient, mocked_redis):
        payload = {
            "agent_name": "Agent007@v1.0.0",
            "peer_id": "QmTestPeerId",
            "addrs": ["/ip4/127.0.0.1/tcp/9000"],
        }

        response = await client.post(f"{self.endpoint}/register", json=payload)
        assert response.status_code == 204

        mocked_redis.get_agents.return_value = [
            {
                "agent_name": "Agent007@v1.0.0",
                "peer_id": "QmTestPeerId",
                "addresses": ["/ip4/127.0.0.1/tcp/9000"],
            }
        ]
        response = await client.get(self.endpoint)
        assert response.status_code == 200
        result = response.json()
        assert result[0]["agent_name"] == "Agent007@v1.0.0"
        assert result[0]["peer_id"] == "QmTestPeerId"
        assert result[0]["addresses"] == ["/ip4/127.0.0.1/tcp/9000"]
