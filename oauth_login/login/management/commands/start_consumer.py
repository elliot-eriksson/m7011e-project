from django.core.management.base import BaseCommand
import pika
import json
from login.consumer import user_lookup  # Import the user_lookup function from consumer.py

class Command(BaseCommand):
    help = 'Start the RabbitMQ consumer for user lookup'

    def handle(self, *args, **kwargs):
        params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
        params.heartbeat = 60  # Sends heartbeats every 60 seconds

        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Declare queues
        channel.queue_declare(queue='user_lookup')

        # Start consuming messages from the 'user_lookup' queue
        channel.basic_consume(queue='user_lookup', on_message_callback=user_lookup, auto_ack=True)
        print("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
