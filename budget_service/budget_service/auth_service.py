# auth_service.py
import requests
from rest_framework.response import Response
from rest_framework import status

class AuthService:
    # OAUTH2_INTROSPECT_URL = "http://localhost:8001/oauth/introspect/"
    OAUTH2_INTROSPECT_URL = "http://localhost:8001/api/custom_introspect/"
    # OAUTH2_INTROSPECT_URL = "http://localhost:8000/api/custom_introspect/"
    CLIENT_ID = "Zx6bjPzYlzArXlKhDbIvNWoIk5LsmZVdcXSpBrSV"  # Replace with your client ID
    CLIENT_SECRET = "wPgMorfcpKEdKlClhqoqeGbPAUrNOYjvxnqsH1k1V6FSdJ0H6WJ9LiUNppTi6SdIb8jOCOAOhfMDdFMMg04lvr1uCRCp6Gxr2t4Iy4LXPMXVdIxUOR4hMk5ixXNP5eef"  # Replace with your client secret


    @staticmethod
    def oauth2_validation(token):
        print("Oauth Validating token")
        try:
            response = requests.post(
                AuthService.OAUTH2_INTROSPECT_URL,
                data={"token": token},
                auth=(AuthService.CLIENT_ID, AuthService.CLIENT_SECRET),
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"valid": False, "error": str(e)}
        
    
    def validate_token(request):
        print("Validating token")
        token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]
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
        return request
