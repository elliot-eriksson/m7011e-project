import pika, json
from decouple import config

RABBITMQ_URL = config('RABBITMQ_URL')
params = pika.URLParameters(RABBITMQ_URL)
params.heartbeat = 600  # Sends heartbeats every 60 seconds

connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body, queue='main'):
    print('publishing to queue', queue)
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)
