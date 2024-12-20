from arrow import now
import pika,json

params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
params.heartbeat = 60  # Sends heartbeats every 60 seconds

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')
channel.queue_declare(queue='user_lookup_response')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    print('Retetrieving budget')

   


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Consuming validation results...\n Exit with CTRL+C')

channel.start_consuming()       

connection.close()    
