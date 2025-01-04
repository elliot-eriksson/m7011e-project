import pika
import json
import pika, json


params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
params.heartbeat = 60  # Sends heartbeats every 60 seconds

connection = pika.BlockingConnection(params)
channel = connection.channel()

def send_account_deletion_message(method, body, queue='account_deletion_queue'):
    print('publishing to queue', queue)
    print('body', body)
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)
    

    print(f" [x] Sent {body}")
    connection.close()
