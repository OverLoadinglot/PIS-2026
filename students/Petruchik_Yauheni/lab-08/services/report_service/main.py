import json
import pika
from rabbitmq_config import get_connection_parameters, get_exchange_name, declare_exchange
from infrastructure.event_bus.rabbitmq_subscriber import ReportSubscriber


def main():
    connection = pika.BlockingConnection(get_connection_parameters())
    channel = connection.channel()
    declare_exchange(channel)
    subscriber = ReportSubscriber(channel)
    subscriber.start()


if __name__ == '__main__':
    main()
