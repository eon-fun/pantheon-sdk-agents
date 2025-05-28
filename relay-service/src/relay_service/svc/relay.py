from libp2p import new_host
from libp2p.relay.circuit_v2.config import RelayConfig
from libp2p.relay.circuit_v2 import CircuitV2Protocol, CircuitV2Transport

from libp2p import NoiseTransport
from libp2p.security.noise.transport import PROTOCOL_ID as NOISE_PROTOCOL_ID
from libp2p.crypto.ed25519 import create_new_key_pair
from multiaddr import Multiaddr
from libp2p.relay.circuit_v2.discovery import (
    RelayDiscovery,
)
from libp2p.relay.circuit_v2.protocol import (
    PROTOCOL_ID,
    STOP_PROTOCOL_ID,
)
from loguru import logger
from relay_service.config import settings


async def start_relay():
    keys = create_new_key_pair()
    host = new_host(
        key_pair=keys,
        sec_opt={NOISE_PROTOCOL_ID: NoiseTransport(keys)},
        listen_addrs=[Multiaddr(settings.relay.url)],
    )
    cfg = RelayConfig(enable_hop=True, enable_stop=True, enable_client=False)
    protocol = CircuitV2Protocol(host, limits=cfg.limits, allow_hop=True)

    # Register protocol handlers on the host
    host.set_stream_handler(PROTOCOL_ID, protocol._handle_hop_stream)
    host.set_stream_handler(STOP_PROTOCOL_ID, protocol._handle_stop_stream)

    discovery = RelayDiscovery(
        host=host,
        auto_reserve=False,
        discovery_interval=cfg.discovery_interval,
        max_relays=cfg.max_relays,
    )
    transport = CircuitV2Transport(host, protocol, cfg)
    transport.discovery = discovery

    relay_id = host.get_id()
    discovery._add_relay = lambda peer_id: discovery._discovered_relays.update(
        {peer_id: None}
    )
    discovery._discovered_relays[relay_id] = None

    logger.info(f"Relay PeerID: {host.get_id()}")
    return host.get_id()
