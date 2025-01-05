import pytest
from .test_utils import mock_validate_token_active, mock_validate_token_inactive

@pytest.fixture
def mock_valid_token():
    with mock_validate_token_active() as mock:
        yield mock

@pytest.fixture
def mock_invalid_token():
    with mock_validate_token_inactive() as mock:
        yield mock


@pytest.mark.django_db
def test_list_budgets_with_valid_token(api_client, test_user, budget, mock_valid_token):
    # Authenticate the request
    api_client.force_authenticate(user=test_user)

    # Simulate session data
    api_client.cookies["sessionid"] = "mock-session"
    api_client.session["user_id"] = test_user.id

    # Make the API request
    response = api_client.get("/budgets/")  # Adjust endpoint path as needed

    # Assert the response
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == budget.id


@pytest.mark.django_db
def test_invalid_token_blocks_access(api_client, mock_invalid_token):
    response = api_client.get("/budgets/", HTTP_AUTHORIZATION="Bearer invalid-token")

    # Assert unauthorized response
    assert response.status_code == 401
    assert "error" in response.data
