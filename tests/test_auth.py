from contextlib import nullcontext

import pytest
from config import Config

class TestAuth:

    @pytest.mark.case_id("AUTH-001")
    @pytest.mark.title("Valid credentials (username:  admin, password: password123)")
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
    @pytest.mark.title("Invalid username")
    def test_auth_invalid_username(self, api_client):
        form_data = {
            "username": "invalid_user",
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code in (200, 401), (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-003")
    @pytest.mark.title("Invalid password")
    def test_auth_invalid_password(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": "wrong_password"
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code in (200, 401), (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-004")
    @pytest.mark.title("Missing username field")
    def test_auth_without_username(self, api_client):
        form_data = {
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code in (200, 401), (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-005")
    @pytest.mark.title("Missing password field")
    def test_auth_without_password(self, api_client):
        form_data = {
            "username": Config.USERNAME
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert auth_response.status_code in (200, 401), (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-006")
    @pytest.mark.title("Empty username")
    def test_auth_with_empty_username(self, api_client):
        form_data = {
            "username": "",
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert auth_response.status_code in (200, 401), (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-007")
    @pytest.mark.title("Empty password")
    def test_auth_with_empty_username(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": ""
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert auth_response.status_code in (200, 401), (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-008")
    @pytest.mark.title("Empty request body")
    def test_auth_with_empty_username(self, api_client):
        form_data = {}
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert auth_response.status_code in (200, 401), (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

    @pytest.mark.case_id("AUTH-009")
    @pytest.mark.title("Null values for credentials")
    def test_auth_with_empty_username(self, api_client):
        form_data = {
            "username": None,
            "password": None
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert auth_response.status_code in (200, 401), (
            f"Expected 401 for invalid credentials, got: {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json, "Response missing 'reason' field"
        assert response_json["reason"] == "Bad credentials", (
            f"Unexpected reason: {response_json['reason']}"
        )

 # (| AUTH-010 | SQL injection in username | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | Security test |)
 # (| AUTH-011 | XSS payload in username | High | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | Security test |)
 # (| AUTH-012 | Very long username &#40;1000+ chars&#41; | Low | **200 OK** | `{"reason": "Bad credentials"}` | ✔️ | Boundary test |)
 # (| AUTH-013 | Special characters in credentials | Medium | **200 OK** | Valid response based on actual credentials | ✔️ | |)
 # (| AUTH-014 | Response time < 2000ms | Medium | **200 OK** | Response within acceptable time | ✔️ | Performance |)
 # (| AUTH-015 | Token format validation | High | **200 OK** | Token is alphanumeric string | ✔️ | Verify token structure |)
 # (| AUTH-016 | Content-Type header validation | Medium | **200 OK** | Response header:  `application/json` | ✔️ | |)
 # (| AUTH-017 | Invalid Content-Type in request | Low | **200/415** | Error or Bad credentials | ✔️ | |)