from django.core.management.base import BaseCommand
import pika
import json
import sys
import signal
from send_email.consumer import send_invitation_email  # Import the user_lookup function from consumer.py

class Command(BaseCommand):
    help = 'Start the RabbitMQ consumer for user lookup'

    def handle(self, *args, **kwargs):
        params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
        params.heartbeat = 600  # Sends heartbeats every 60 seconds

        connection = pika.BlockingConnection(params)

        channel = connection.channel()


        channel.queue_declare(queue='send_email_invitations')

        channel.basic_consume(queue='send_email_invitations', on_message_callback=send_invitation_email, auto_ack=True)
        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        

def graceful_shutdown(signum, frame):
    print("Shutting down gracefully...")
    # Perform cleanup here (e.g., closing connections, saving state)
    sys.exit(0)

# Attach signal handlers
signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)