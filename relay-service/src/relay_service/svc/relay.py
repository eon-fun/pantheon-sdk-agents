# from libp2p import new_host
# from libp2p.relay.circuit_v2 import RelayConfig, CircuitV2Protocol, CircuitV2Transport
# from libp2p.transport.tcp.tcp import TCP
# from libp2p.security.noise.transport import NoiseTransport
# from libp2p.peer.id import ID
# from libp2p.crypto.keys import create_new_key_pair
# from multiaddr import Multiaddr
# import asyncio
from loguru import logger


async def start_relay():
    # priv, pub = create_new_key_pair()

    # # Create a new libp2p host
    # host = await new_host(
    #     transport_opt=[TCP()],
    #     sec_opt=[NoiseTransport(priv)],
    #     identity=priv,
    #     listen_addrs=[Multiaddr("/ip4/0.0.0.0/tcp/9000")]
    # )

    # cfg = RelayConfig(enable_hop=True, enable_stop=True, enable_client=False)
    # proto = CircuitV2Protocol(host, allow_hop=True, limits=cfg.limits)
    # transport = CircuitV2Transport(host, proto, config=cfg)
    # host.add_transport(transport)
    # await host.start()

    logger.info("Relay PeerID: ...")
