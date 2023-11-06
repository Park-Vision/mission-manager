import asyncio
import json
from confluent_kafka import Producer, Consumer
import config

class KafkaConnector:
    def __init__(self, server: str, command_callbacks: dict) -> None:
        self.producer = Producer({"bootstrap.servers": server})
        self.consumer = Consumer({
        'bootstrap.servers': server,
        'group.id': 'parkVision',
        'auto.offset.reset': 'earliest'
        })
        self.command_callbacks = command_callbacks

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            print("Message delivery failed: {}".format(err))
        else:
            print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

    def send_one(self, data):
        # Trigger any available delivery report callbacks from previous produce() calls
        self.producer.poll(0)

        # Asynchronously produce a message. The delivery report callback will
        # be triggered from the call to poll() above, or flush() below, when the
        # message has been successfully delivered or failed permanently.
        self.producer.produce(
            "drones-info", data.encode("utf-8"), callback=self.delivery_report, key=str(config.DRONE_ID)
        )

    def flush(self):
        self.producer.flush()

    async def consume_messages(self):
        """Async consume messages on assigned topic, when message is received, callback"""
        self.consumer.subscribe([f'drone-{config.DRONE_ID}'])
        print("Subscribed to drone topic")


        while True:
            loop = asyncio.get_running_loop()
            msg = await loop.run_in_executor(None, self.consumer.poll, 1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            msg_value = msg.value().decode('utf-8')
            print('Received message: {}'.format(msg_value))
            
            # TODO remove------
            if msg_value == "start":
                self.send_one(json.dumps({"Lat": 51, "Lon": 17}))
            # end to remove----

            # react to command, by executing drone function
            # assigned to command content
            try:
                self.command_callbacks[msg_value]()
            except KeyError:
                print(f"Invalid command from operator: {msg_value}")
                continue

    def close_consumer(self):
        self.consumer.close()
