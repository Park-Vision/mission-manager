from confluent_kafka import Producer


class KafkaConnector:
    def __init__(self) -> None:
        self.producer = Producer({"bootstrap.servers": "localhost:9092"})

    def delivery_report(err, msg):
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
            "quickstart-events", data.encode("utf-8"), callback=self.delivery_report
        )

    def flush(self):
        self.producer.flush()
