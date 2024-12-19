from budget.producer import channel, publish
import json
import time

def getUserID(username=None, email=None):
    payload = {}
    if username:
        payload['username'] = username
    if email:
        payload['email'] = email
    
    if not payload:
        raise ValueError("At least one of username or email must be provided.")
    
    publish("user.lookup", payload, "user_lookup")

    user_id_response = None
    for _ in range(1000):
        print("Waiting for response...")
        method_frame, properties, body = channel.basic_get(queue='user_lookup_response', auto_ack=True)
        if body:
            response = json.loads(body)
            user_id_response = response.get('user_id')
            break
        time.sleep(0.5)  # Wait before checking again (polling)


    if user_id_response is None:
        raise Exception("User lookup failed.")

    return user_id_response
