import asyncio
import json

from manager import config
from confluent_kafka import Consumer, Producer

ssl_config = {
   #"metadata.broker.list": at_least_one_of_the_brokers,
   'metadata.broker.list': 'SSL://127.0.0.1:29092',
   "security.protocol": "SSL",
   # CA certificate file for verifying the broker's certificate.
   "ssl.ca.location": "ssl/ca-cert",
   # Client's certificate
   "ssl.certificate.location": "ssl/client_drone_client.pem",
   # Client's key
   "ssl.key.location": "ssl/client_drone_client_v2.key",
   # Key password, if any.
   "ssl.key.password": "maciek",
   "ssl.endpoint.identification.algorithm": "none",
}


class KafkaConnector:
    def __init__(self, server: str, command_callbacks: dict) -> None:
        prod_config = {"bootstrap.servers": server}
        prod_config.update(ssl_config)

        con_config = {
                "bootstrap.servers": server,
                "group.id": "drones",
                "auto.offset.reset": "earliest",
                }
        con_config.update(ssl_config)

        self.producer = Producer(prod_config)
        self.consumer = Consumer(con_config)
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
            "drones-info",
            data.encode("utf-8"),
            callback=self.delivery_report,
            key=str(config.DRONE_ID),
        )

    def flush(self):
        self.producer.flush()

    async def consume_messages(self):
        """Async consume messages on assigned topic, when message is received, callback"""
        # self.consumer.subscribe([f"drone-{config.DRONE_ID}"]) # TODO change topic
        self.consumer.subscribe([f"drones-info"])
        print("Subscribed to drone topic")

        while True:
            loop = asyncio.get_running_loop()
            msg = await loop.run_in_executor(None, self.consumer.poll, 1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            msg_value = msg.value().decode("utf-8")
            print("Received message: {}".format(msg_value))

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
