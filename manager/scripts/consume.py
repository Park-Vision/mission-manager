import json
import asyncio

from manager.telemetry.kafka_connection import KafkaConnector
async def con(connector):
    await connector.consume_messages()

connector = KafkaConnector("127.0.0.1:29092", {})
for i in range(3):
    connector.send_one(json.dumps({"Lat": 69, "Lon": 69}))
asyncio.run(con(connector))
