from send_email.producer import channel, publish
import json
import time

def getStaffStatus(userID):
    payload = {}

    payload['user_id'] = userID

    
    publish("staff.lookup", payload, "staff_lookup")


    for _ in range(1000):
        print("Waiting for response...")
        method_frame, properties, body = channel.basic_get(queue='staff_lookup_response', auto_ack=True)
        if body:
            response = json.loads(body)
            print("Response received:", response)
            isStaff = response.get('is_staff')
            break
        time.sleep(0.5)  # Wait before checking again (polling)


    if isStaff is None:
        return False

    return isStaff
