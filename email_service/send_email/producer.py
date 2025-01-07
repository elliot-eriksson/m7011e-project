import pika, json

params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
params.heartbeat = 600  # Sends heartbeats every 60 seconds

connection = pika.BlockingConnection(params)
channel = connection.channel()


#token_validation_queue
def publish(method, body, routing_key):
    print('publishing to other service')
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=routing_key, body=json.dumps(body), properties=properties)
