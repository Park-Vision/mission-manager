import json
from confluent_kafka import Producer, Consumer
from telemetry.kafka_connection import KafkaConnector

connector = KafkaConnector('localhost:9092')

connector.send_one(json.dumps({"Lat": 51, "Lon": 17}))
connector.consume_messages()
