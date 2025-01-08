import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .token_utils import validate_token
from .producer import publish

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


    try: 
        if username:
            user = User.objects.get(username=username)
        elif email:
            user = User.objects.get(email=email)
        user_id = user.id
        user_email = user.email

        response_body = json.dumps({"user_id": user_id, "user_email": user_email})
        channel.basic_publish(
            exchange='',
            routing_key='user_lookup_response',
            body=response_body
        )

    except ObjectDoesNotExist as e:
        response_body = json.dumps({"error": "User not found."})
        channel.basic_publish(
            exchange='',
            routing_key='user_lookup_response',
            body=response_body
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

def process_oauth2_validation(ch, method, properites, body):
    print("Processing token validation request in oauth")
    message = json.loads(body)
    token = message.get("token")

    if not token:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    result = validate_token(token)
    publish('token.validated',result, 'token_result_queue')


def lookupStaffStatus(channel, method, properties, body):
    message = json.loads(body)
    userID = message.get("user_id")

    user = User.objects.get(id=userID)
    is_staff = user.is_staff
    response_body = json.dumps({"is_staff": is_staff})
    channel.basic_publish(
        exchange='',
        routing_key='staff_lookup_response',
        body=response_body
    )