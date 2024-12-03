from arrow import now
import pika,json
import requests
# from oauth2_provider.models import AccessToken


paramas = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')

connection = pika.BlockingConnection(paramas)
channel = connection.channel()

channel.queue_declare(queue='token_validation_queue')
channel.queue_declare(queue='validation_result_queue')

OAUTH2_INTROSPECT_URL = "http://localhost:8000/oauth/introspect/"
CLIENT_ID = "Zx6bjPzYlzArXlKhDbIvNWoIk5LsmZVdcXSpBrSV"  # Replace with your client ID
CLIENT_SECRET = "wPgMorfcpKEdKlClhqoqeGbPAUrNOYjvxnqsH1k1V6FSdJ0H6WJ9LiUNppTi6SdIb8jOCOAOhfMDdFMMg04lvr1uCRCp6Gxr2t4Iy4LXPMXVdIxUOR4hMk5ixXNP5eef"  # Replace with your client secret

def validate_token(token):
    """
    Validate the token using OAuth2 introspection endpoint or JWT decoding.
    """
    
    # access_token = AccessToken.objects.get(token=token, expires__gt=now())
    # print("Access token:", access_token)
    try:
        response = requests.post(
            OAUTH2_INTROSPECT_URL,
            data={"token": token},
            auth=(CLIENT_ID, CLIENT_SECRET)
        )
        print("Response data:", response.json())
        response_data = response.json()
        if response.status_code == 200 and response_data.get("active"):
            return {"valid": True, "user_id": response_data.get("username")}
        else:
            return {"valid": False, "error": "Invalid or expired token"}

    except Exception as e:
        return {"valid": False, "error": str(e)}
    
def on_message(channel, method, properties, body):
    """
    Process a message from the token_validation_queue.
    """
    print("Received message:", body)
    message = json.loads(body)

    token = message.get("token")
    if not token:
        print("No token provided in message.")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Validate the token
    result = validate_token(token)

    # Publish the result to the validation_result_queue
    channel.basic_publish(
        exchange='',
        routing_key='validation_result_queue',
        body=json.dumps(result)
    )
    print("Validation result sent:", result)

    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming
channel.basic_consume(queue='token_validation_queue', on_message_callback=on_message)
print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()