import pika, json

paramas = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')

connection = pika.BlockingConnection(paramas)
channel = connection.channel()

def publish(method, body):
    print('publishing to admin')
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='token_validation_queue', body=json.dumps(body), properties=properties)


    # connection.close()