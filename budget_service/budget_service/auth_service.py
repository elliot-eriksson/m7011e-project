# auth_service.py
import requests

class AuthService:
    # OAUTH2_INTROSPECT_URL = "http://localhost:8001/oauth/introspect/"
    OAUTH2_INTROSPECT_URL = "http://localhost:8001/api/custom_introspect/"
    CLIENT_ID = "Zx6bjPzYlzArXlKhDbIvNWoIk5LsmZVdcXSpBrSV"  # Replace with your client ID
    CLIENT_SECRET = "wPgMorfcpKEdKlClhqoqeGbPAUrNOYjvxnqsH1k1V6FSdJ0H6WJ9LiUNppTi6SdIb8jOCOAOhfMDdFMMg04lvr1uCRCp6Gxr2t4Iy4LXPMXVdIxUOR4hMk5ixXNP5eef"  # Replace with your client secret


    @staticmethod
    def validate_token(token):
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
