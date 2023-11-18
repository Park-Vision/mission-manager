import json
import asyncio

from manager.telemetry.kafka_connection import KafkaConnector
from manager.config import PARKVISION_SERVER

async def con(connector):
    await connector.consume_messages()

connector = KafkaConnector(PARKVISION_SERVER, {})
#for i in range(3):
    #connector.send_one(json.dumps({"Lat": 69, "Lon": 69}))
asyncio.run(con(connector))
