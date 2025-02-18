from django.core.management.base import BaseCommand
import pika
import sys
import signal
from login.consumer import user_lookup, process_oauth2_validation, lookupStaffStatus  
from decouple import config

RABBITMQ_URL = config('RABBITMQ_URL')


class Command(BaseCommand):
    help = 'Start the RabbitMQ consumer for user lookup'

    def handle(self, *args, **kwargs):
        params = pika.URLParameters(RABBITMQ_URL)
        params.heartbeat = 600  # Sends heartbeats every 60 seconds

        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Declare queues
        channel.queue_declare(queue='user_lookup')
        channel.queue_declare(queue='token_validation_queue')
        channel.queue_declare(queue='token_result_queue')
        channel.queue_declare(queue='staff_lookup')
        channel.queue_declare(queue='staff_lookup_response')

        

        # Start consuming messages from the 'user_lookup' queue
        channel.basic_consume(queue='user_lookup', on_message_callback=user_lookup, auto_ack=True)
        channel.basic_consume(queue='token_validation_queue', on_message_callback=process_oauth2_validation, auto_ack=True)
        channel.basic_consume(queue='staff_lookup', on_message_callback=lookupStaffStatus, auto_ack=True)
        print("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
        

def graceful_shutdown(signum, frame):
    print("Shutting down gracefully...")
    sys.exit(0)

# Attach signal handlers
signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)