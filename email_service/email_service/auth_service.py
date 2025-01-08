from send_email.producer import channel, publish
import json
import time
from rest_framework.response import Response
from rest_framework import status
from decouple import config
class AuthService:
    CLIENT_ID = config("CLIENT_ID")
    CLIENT_SECRET = config("CLIENT_SECRET")

    @staticmethod
    def oauth2_validation(token):
        print("Oauth Validating token")
        message = {"token": token}
        try:
            print("Publishing token for validation")
            print("message: ", message)

            publish('token.validate', message, 'token_validation_queue')
            print("Token published for validation")
            for _ in range(100):
                method_frame, properties, body = channel.basic_get(queue='token_result_queue', auto_ack=True)
                if body:
                    print("Response received:", body)
                    response = json.loads(body)
                    print("Response received:", response)
            time.sleep(0.5) 
            
            return response
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def validate_token(request):
        print("Validating token")
        print("Request META AUTHORIZATION SPLIT: ", request.META.get('HTTP_AUTHORIZATION', '').split('Bearer '))
        token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]
        print("Token: ", token)
        if not token:
            return Response(
                {'error': 'Authorization token not provided'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        valid_token = AuthService.oauth2_validation(token)
        print(f"Token validation result: {valid_token}")
        if not valid_token.get('active'):
            return Response(
                {'error': valid_token.get('error', 'Unauthorized')},
                status=status.HTTP_401_UNAUTHORIZED,
            )
               
        request.session["user_id"] = valid_token.get("user_id")
        request.session["username"] = valid_token.get("username")
        return request
