import json
import pika
from rabbitmq_config import get_connection_parameters, get_exchange_name, declare_exchange


def publish_transaction_event(transaction):
    connection = pika.BlockingConnection(get_connection_parameters())
    channel = connection.channel()
    declare_exchange(channel)
    message = json.dumps(transaction)
    channel.basic_publish(
        exchange=get_exchange_name(),
        routing_key='transaction.added',
        body=message,
    )
    connection.close()


def main():
    sample_event = {
        'budget_id': 'b49',
        'transaction_id': 't1',
        'amount': 120.0,
        'currency': 'RUB',
        'category': 'Продукты',
        'member': 'Мама',
        'type': 'expense',
    }
    publish_transaction_event(sample_event)


if __name__ == '__main__':
    main()
