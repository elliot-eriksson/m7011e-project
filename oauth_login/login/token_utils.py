from oauth2_provider.models import get_access_token_model, get_refresh_token_model
from django.utils.timezone import now


def validate_token(token):
    try:
        token = token.strip()  # Remove leading and trailing whitespaces

        AccessToken = get_access_token_model()
        access_token = AccessToken.objects.filter(token=token).first()

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

def revoke_token(user_id):
    try:
        AccessToken = get_access_token_model()
        RefreshToken = get_refresh_token_model()
        AccessToken.objects.filter(user=user_id).delete()
        RefreshToken.objects.filter(user=user_id).delete()
    except AccessToken.DoesNotExist:
        pass
