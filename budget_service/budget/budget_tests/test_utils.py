from unittest.mock import patch

# Mock for AuthService.validate_token
def mock_validate_token_active():
    """
    Returns a patch where AuthService.validate_token always validates the token as active.
    """
    return patch("budget_service.auth_service.AuthService.validate_token", return_value={
        "active": True,
        "user_id": 1,
        "username": "testuser",
    })


def mock_validate_token_inactive():
    """
    Returns a patch where AuthService.validate_token always validates the token as inactive.
    """
    return patch("budget_service.auth_service.AuthService.validate_token", return_value={
        "active": False,
    })
