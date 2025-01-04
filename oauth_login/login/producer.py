import pika, json


params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
params.heartbeat = 60  # Sends heartbeats every 60 seconds

connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body, queue='main'):
    print('publishing to queue', queue)
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)
    


    # connection.close()