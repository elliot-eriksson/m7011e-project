import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
# from login.views import UserDetail  # Adjust the import based on your actual model location

def user_lookup(channel, method, properties, body):
    """
    Process a message from the user_lookup queue.
    """
    print("Received message:", body)
    message = json.loads(body)

    username = message.get("username")
    email = message.get("email")

    if not username and not email:
        print("No username or email provided in message.")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Lookup the user
    try: 
        if username:
            user = User.objects.get(username=username)
            print("User found:", user)
        elif email:
            user = User.objects.get(email=email)
            print("User found:", user)
        user_id = user.id
        print("User ID:", user_id)
        user_email = user.email
        print("User email:", user_email)

        response_body = json.dumps({"user_id": user_id, "user_email": user_email})
        print("innan publish.")
        channel.basic_publish(
            exchange='',
            routing_key='user_lookup_response',
            body=response_body
        )
        print("innan ack.")
        # channel.basic_ack(delivery_tag=method.delivery_tag)
    except ObjectDoesNotExist as e:
        print("User not found:", e)
        response_body = json.dumps({"error": "User not found."})
        channel.basic_publish(
            exchange='',
            routing_key='user_lookup_response',
            body=response_body
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)
