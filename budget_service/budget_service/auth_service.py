# auth_service.py
import requests
# from budget_service.budget.producer import publish, channel
from budget.producer import channel, publish
import json
import time
from rest_framework.response import Response
from rest_framework import status

class AuthService:
    # OAUTH2_INTROSPECT_URL = "http://localhost:8001/oauth/introspect/"
    # OAUTH2_INTROSPECT_URL = "http://localhost:8001/api/custom_introspect/"
    
    OAUTH2_INTROSPECT_URL = "http://0.0.0.0:8001/api/custom_introspect/"

    # OAUTH2_INTROSPECT_URL = "http://localhost:8000/api/custom_introspect/"
    CLIENT_ID = "Zx6bjPzYlzArXlKhDbIvNWoIk5LsmZVdcXSpBrSV"  # Replace with your client ID
    CLIENT_SECRET = "wPgMorfcpKEdKlClhqoqeGbPAUrNOYjvxnqsH1k1V6FSdJ0H6WJ9LiUNppTi6SdIb8jOCOAOhfMDdFMMg04lvr1uCRCp6Gxr2t4Iy4LXPMXVdIxUOR4hMk5ixXNP5eef"  # Replace with your client secret


    @staticmethod
    def oauth2_validation(token):
        print("Oauth Validating token")
        message = {"token": token}
        try:
            print("Publishing token for validation")
            print("message: ", message)

            publish('token.validate', message, 'token_validation_queue')
            for _ in range(100):
                # print("Waiting for response...")
                method_frame, properties, body = channel.basic_get(queue='token_result_queue', auto_ack=True)
                if body:
                    response = json.loads(body)
                    print("Response received:", response)
                    # user_id_response = response.get('valid')
            time.sleep(0.5)  # Wait before checking again (polling)
            return response
            # return {"valid": True, "message": "Token sent for validation"}
        except Exception as e:
            return {"valid": False, "error": str(e)}
            # user_id_response = None

        # try:
        #     response = requests.post(
        #         AuthService.OAUTH2_INTROSPECT_URL,
        #         data={"token": token},
        #         auth=(AuthService.CLIENT_ID, AuthService.CLIENT_SECRET),
        #     )
        #     response.raise_for_status()
        #     return response.json()
        # except requests.RequestException as e:
        #     return {"valid": False, "error": str(e)}
        
    
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
