import asyncio
import json
from pills_crawler.settings import NATS_CLIENT_ID, NATS_CLUSTER_ID
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN


class NatsPublisher:

    def __init__(self):
        pass

    async def pub_nats(self, loop, msg):
        nc = NATS()
        await nc.connect(io_loop=loop)
        sc = STAN()
        await sc.connect(NATS_CLUSTER_ID, NATS_CLIENT_ID, nats=nc)

        # Synchronous Publisher, does not return until an ack
        # has been received from NATS Streaming.
        await sc.publish("medicine.crawler", json.dumps(msg).encode('utf-8'))

    def pub(self, msg):
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
        loop.run_until_complete(self.pub_nats(loop, msg))
        loop.close()
