import pytest
from config import Config

# Test the /auth endpoint to ensure the API is running.
class TestAuth:

    @pytest.mark.case_id("AUTH-001")
    def test_auth_status_response(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code in (200, 201), (
            f"Unexpected status code: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "token" in response_json, "Response missin g 'token' field"
        assert isinstance(response_json["token"], str), (
            f"Token is not a string: {type(response_json['token'])}"
        )
        assert len(response_json["token"]) > 0, "Token is empty"

    @pytest.mark.case_id("AUTH-002")

    def test_auth_invalid_username(self, api_client):
        form_data = {
            "username": "invalid_user",
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code == 401, (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-003")
    def test_auth_invalid_password(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": "wrong_password"
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code == 401, (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-004")
    def test_auth_without_username(self, api_client):
        form_data = {
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code == 401, (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-005")
    def test_auth_without_password(self, api_client):
        form_data = {
            "username": Config.USERNAME
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert auth_response.status_code == 401, (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-006")
    def test_auth_without_password(self, api_client):
        form_data = {
            "username": Config.USERNAME
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert auth_response.status_code == 401, (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )