import json


class NotificationSubscriber:
    def __init__(self, channel):
        self.channel = channel

    def on_message(self, ch, method, properties, body):
        event = json.loads(body)
        print(f"Notification Service: уведомление для семьи — новая транзакция {event}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.queue_declare(queue='notification_service_queue', durable=True)
        self.channel.queue_bind(queue='notification_service_queue', exchange='budget_events', routing_key='transaction.added')
        self.channel.basic_consume(queue='notification_service_queue', on_message_callback=self.on_message)
        self.channel.start_consuming()
