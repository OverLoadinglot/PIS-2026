import pika
import json
from rabbitmq_config import get_connection_parameters, get_exchange_name, declare_exchange


class RabbitMQPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(get_connection_parameters())
        self.channel = self.connection.channel()
        declare_exchange(self.channel)

    def publish(self, routing_key: str, payload: dict):
        self.channel.basic_publish(
            exchange=get_exchange_name(),
            routing_key=routing_key,
            body=json.dumps(payload),
        )

    def close(self):
        self.connection.close()
