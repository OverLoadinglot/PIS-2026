import pika


def get_connection_parameters():
    return pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        heartbeat=600,
        blocked_connection_timeout=300,
    )


def get_exchange_name():
    return 'budget_events'


def declare_exchange(channel):
    channel.exchange_declare(
        exchange=get_exchange_name(),
        exchange_type='topic',
        durable=True,
    )
