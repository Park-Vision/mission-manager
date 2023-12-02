import asyncio

from manager.config import PARKVISION_SERVER
from manager.telemetry.kafka_connection import KafkaConnector


async def con(connector):
    await connector.consume_messages()

connector = KafkaConnector(PARKVISION_SERVER, {})

asyncio.run(con(connector))
