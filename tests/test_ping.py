import pytest
from config import Config

# Test the /ping endpoint to ensure the API is running.
class TestPing:
    def test_healthcheck_status(self, api_client, ping_response):
        assert ping_response.status_code in (200, 201), (
            f"Unexpected status code: {ping_response.status_code}"
        )

    def test_healthcheck_response_message(self, api_client, ping_response):
        assert ping_response.text in ("OK", "Created"), (
            f"Unexpected response body: {ping_response.text!r}"
        )

    def test_healthcheck_content_type(self, api_client, ping_response):
        assert "Content-Type" in ping_response.headers, "Missing 'Content-Type' header"
        assert ping_response.headers["Content-Type"].strip(), "Content-Type header is empty"

    def test_healthcheck_no_auth(self, api_client):
        response = api_client.get(Config.PING_ENDPOINT, headers={})
        assert response.status_code not in (401, 403), (
            f"Endpoint should be accessible without auth, got {response.status_code}"
        )
        assert "WWW-Authenticate" not in response.headers, "Server advertised authentication challenge"
        assert response.status_code in (200, 201), f"Unexpected success status: {response.status_code}"
        assert response.text in ("OK", "Created"), f"Unexpected response body: {response.text!r}"
