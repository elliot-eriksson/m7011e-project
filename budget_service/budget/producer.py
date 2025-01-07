import pika, json

params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
params.heartbeat = 600  # Sends heartbeats every 60 seconds

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='user_lookup_response')
channel.queue_declare(queue='token_result_queue')

#token_validation_queue
def publish(method, body, routing_key):
    print('publishing to other service')
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=routing_key, body=json.dumps(body), properties=properties)


    # connection.close()


# import pika
# import json

# def publish_message(exchange, routing_key, message):
#     """
#     Publishes a message to a RabbitMQ exchange with a given routing key.

#     :param exchange: The name of the RabbitMQ exchange.
#     :param routing_key: The routing key to determine the queue.
#     :param message: The message body (dictionary) to be sent.
#     """
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()

#     # Declare the exchange (if it doesn’t already exist)
#     channel.exchange_declare(exchange=exchange, exchange_type='direct')

#     # Serialize the message to JSON
#     body = json.dumps(message)

#     # Publish the message
#     channel.basic_publish(
#         exchange=exchange,
#         routing_key=routing_key,
#         body=body
#     )

#     print(f" [x] Sent message to exchange '{exchange}' with routing key '{routing_key}': {message}")
#     connection.close()


# def publish_user_lookup(username=None, email=None):
#     message = {'username': username, 'email': email}
#     publish_message('user_lookup', 'fetch_user', message)

# def publish_notification(to, subject, body):
#     message = {'to': to, 'subject': subject, 'body': body}
#     publish_message('notifications', 'send_email', message)


# publish_message(
#     exchange='user_lookup',
#     routing_key='fetch_user',
#     message={'username': 'john_doe', 'email': None}
# )

# publish_user_lookup(username='john_doe', email=None)

# publish_message(
#     exchange='notifications',
#     routing_key='send_email',
#     message={'to': 'john_doe@example.com', 'subject': 'Welcome!', 'body': 'Hello, John!'}
# )
