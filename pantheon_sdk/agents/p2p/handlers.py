from __future__ import annotations

import datetime
import json
from typing import TYPE_CHECKING

import httpx
from loguru import logger

from pantheon_sdk.agents.p2p.const import PROTOCOL_CARD, PROTOCOL_DELEGATE

if TYPE_CHECKING:
    from libp2p.network.stream.net_stream import INetStream

    from pantheon_sdk.agents import abc


async def handle_card(stream: INetStream) -> None:
    peer_id_obj = stream.muxed_conn.peer_id
    peer_id_str = str(peer_id_obj) if peer_id_obj else "UnknownPeer"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    logger.info(f"[{timestamp}] Received card request on {PROTOCOL_CARD} from peer {peer_id_str}")

    card_url = "http://localhost:8000/card"

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(card_url)
            response.raise_for_status()

        await stream.write(response.content)
        logger.info(f"[{timestamp}] Sent card data to peer {peer_id_str} for protocol {PROTOCOL_CARD}")

    except httpx.HTTPStatusError as e:
        logger.error(
            f"[{timestamp}] HTTP error for {PROTOCOL_CARD} from {peer_id_str}: {e.response.status_code} - {e.response.text}"
        )
        error_msg = f'{{"error":"HTTP error: {e.response.status_code}","code":{e.response.status_code}}}'.encode()
        await stream.write(error_msg)
    except httpx.RequestError as e:
        logger.error(
            f"[{timestamp}] Request error for {PROTOCOL_CARD} from {peer_id_str}: {type(e).__name__} - {str(e)}"
        )
        await stream.write(b'{"error":"Request to /card failed or timed out","code":504}')  # 504 Gateway Timeout
    except Exception as e:
        logger.error(f"[{timestamp}] Unexpected error processing {PROTOCOL_CARD} for {peer_id_str}: {e}", exc_info=True)
        await stream.write(b'{"error":"Internal server error","code":500}')
    finally:
        try:
            await stream.close()
        except Exception as e:
            logger.error(f"[{timestamp}] Error closing stream for {PROTOCOL_CARD} with peer {peer_id_str}: {e}")
        logger.info(f"[{timestamp}] Closed stream for {PROTOCOL_CARD} with peer {peer_id_str}")


async def handle_delegate(stream: INetStream, agent: abc.AbstractAgent) -> None:
    peer_id_obj = stream.muxed_conn.peer_id
    peer_id_str = str(peer_id_obj) if peer_id_obj else "UnknownPeer"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    logger.info(f"[{timestamp}] Received delegate request on {PROTOCOL_DELEGATE} from peer {peer_id_str}")

    try:
        data = await stream.read()
        payload = json.loads(data.decode("utf-8"))

        goal = payload.get("goal")
        plan = payload.get("plan")

        if not goal:
            raise ValueError("Goal is required in delegate payload")

        result = await agent.handle(goal=goal, plan=plan)

        response = json.dumps(result.model_dump()).encode("utf-8")
        await stream.write(response)

        logger.info(f"[{timestamp}] Successfully handled delegate request from peer {peer_id_str}")

    except Exception as e:
        logger.error(f"[{timestamp}] Error handling delegate request from {peer_id_str}: {e}")
        error_response = json.dumps({"error": str(e), "code": 500}).encode("utf-8")
        await stream.write(error_response)
    finally:
        try:
            await stream.close()
        except Exception as e:
            logger.error(f"[{timestamp}] Error closing delegate stream with peer {peer_id_str}: {e}")
        logger.info(f"[{timestamp}] Closed delegate stream with peer {peer_id_str}")
