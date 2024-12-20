from django.core.management.base import BaseCommand
import pika
import json
from send_email.consumer import send_invitation_email  # Import the user_lookup function from consumer.py

class Command(BaseCommand):
    help = 'Start the RabbitMQ consumer for user lookup'

    def handle(self, *args, **kwargs):
        params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
        params.heartbeat = 60  # Sends heartbeats every 60 seconds

        connection = pika.BlockingConnection(params)

        channel = connection.channel()

        # channel.exchange_declare(exchange='invitations', exchange_type='fanout')
        channel.queue_declare(queue='send_email_invitations')

        # result = channel.queue_declare(queue='', exclusive=True)
        # queue_name = result.method.queue
        # channel.queue_bind(exchange='invitations', queue=queue_name)

        channel.basic_consume(queue='send_email_invitations', on_message_callback=send_invitation_email, auto_ack=True)
        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
