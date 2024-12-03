from arrow import now
import pika,json
import requests
# from oauth2_provider.models import AccessToken


paramas = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')

connection = pika.BlockingConnection(paramas)
channel = connection.channel()

channel.queue_declare(queue='validation_result_queue')

def on_validation_result(channel, method, properties, body):
    """
    Process a message from the validation_result_queue.
    """
    print("Received message:", body)
    message = json.loads(body)

    # Send the validation result to the client
    print("Sending validation result to client:", message)

    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='validation_result_queue', on_message_callback=on_validation_result)
print('Consuming validation results...')
channel.start_consuming()