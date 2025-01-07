from django.core.management.base import BaseCommand
import pika
import sys
import signal
from budget.consumer import callback, delete_user_budget

class Command(BaseCommand):
    help = 'Start the RabbitMQ consumer for user lookup'

    def handle(self, *args, **kwargs):
        params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
        params.heartbeat = 600  # Sends heartbeats every 600 seconds

        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue='main')
        channel.queue_declare(queue='user_lookup_response')
        channel.queue_declare(queue='delete_user_budget')

        channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue='delete_user_budget', on_message_callback=delete_user_budget, auto_ack=True)

        print('Consuming validation results...\n Exit with CTRL+C')

        channel.start_consuming()       


def graceful_shutdown(signum, frame):
    print("Shutting down gracefully...")
    # Perform cleanup here (e.g., closing connections, saving state)
    sys.exit(0)

# Attach signal handlers
signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

