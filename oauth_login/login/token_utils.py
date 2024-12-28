from datetime import datetime
# from oauth2_provider.models import AccessToken

from oauth2_provider.models import get_access_token_model
from django.utils.timezone import now


def validate_token(token2):
    try:
        print(f"Token received: {token2}")

        token2 = token2.strip()  # Remove leading and trailing whitespaces
        print(f"Token strip: {token2}")


        AccessToken = get_access_token_model()
        print(f"Access token model: {AccessToken}")
        # Now you can query the model as usual
        # access_token = AccessToken.objects.get(token=token)
        # print(f"Access token: {AccessToken.objects.filter(token=token)}")
        print("token2 type:", type(token2))
        # token2 = "VawHqlhJhNOgyBEBxh51zQGyTNmsbm"
        access_token = AccessToken.objects.filter(token=token2).first()


        # access_token = AccessToken.objects.get(token=token)
        print("Access token found:", access_token)
        if access_token.expires > now():
            return {
                "valid": True,
                "active": True,
                "user_id": access_token.user_id,
                "username": access_token.user.username,
            }
        else:
            return {"valid": False, "error": "Token expired or revoked."}
    except Exception as e:
        return {"valid": False, "error": str(e)}
    # except AccessToken.DoesNotExist:
    #     return {"valid": False, "error": "Token not found."}