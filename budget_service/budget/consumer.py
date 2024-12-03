from arrow import now
import pika,json
import requests
# from oauth2_provider.models import AccessToken



# def validate_token_with_auth_service(token):
#     OAUTH2_INTROSPECT_URL = "http://localhost:8001/oauth/introspect/"
#     CLIENT_ID = "Zx6bjPzYlzArXlKhDbIvNWoIk5LsmZVdcXSpBrSV"  # Replace with your client ID
#     CLIENT_SECRET = "wPgMorfcpKEdKlClhqoqeGbPAUrNOYjvxnqsH1k1V6FSdJ0H6WJ9LiUNppTi6SdIb8jOCOAOhfMDdFMMg04lvr1uCRCp6Gxr2t4Iy4LXPMXVdIxUOR4hMk5ixXNP5eef"  # Replace with your client secret

    
#     try:
#         response = requests.post(
#             OAUTH2_INTROSPECT_URL,
#             data={"token": token},
#             auth=(CLIENT_ID, CLIENT_SECRET)
#         )
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         return {"valid": False, "error": str(e)}


def on_message(channel, method, properties, body):
    print("Received message:", body)
    message = json.loads(body)

    token = message.get("token")
    if not token:
        print("No token provided in message.")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    validation_result = validate_token_with_auth_service(token)
    if not validation_result.get("valid"):
        print("Invalid token:", validation_result.get("error"))
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Proceed with processing the message
    print("Processing message:", message)

    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)

paramas = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')

connection = pika.BlockingConnection(paramas)
channel = connection.channel()

channel.queue_declare(queue='validation_result_queue')


channel.basic_consume(queue='validation_result_queue', on_message_callback=on_message)
print('Consuming validation results...')
channel.start_consuming()