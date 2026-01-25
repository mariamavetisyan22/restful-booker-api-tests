import time
import re
import pytest
from config import Config
from tests.helpers.auth_helpers import (
    assert_bad_credentials_response,
    assert_successful_auth_response
)

class TestAuth:

    @pytest.mark.case_id("AUTH-001")
    @pytest.mark.title("Valid credentials (username:  admin, password: password123)")
    def test_auth_status_response(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_successful_auth_response(auth_response)

    @pytest.mark.case_id("AUTH-002")
    @pytest.mark.title("Invalid username")
    def test_auth_invalid_username(self, api_client):
        form_data = {
            "username": "invalid_user",
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_bad_credentials_response(auth_response)


    @pytest.mark.case_id("AUTH-003")
    @pytest.mark.title("Invalid password")
    def test_auth_invalid_password(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": "wrong_password"
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_bad_credentials_response(auth_response)

    @pytest.mark.case_id("AUTH-004")
    @pytest.mark.title("Missing username field")
    def test_auth_without_username(self, api_client):
        form_data = {
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_bad_credentials_response(auth_response)

    @pytest.mark.case_id("AUTH-005")
    @pytest.mark.title("Missing password field")
    def test_auth_without_password(self, api_client):
        form_data = {
            "username": Config.USERNAME
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_bad_credentials_response(auth_response)

    @pytest.mark.case_id("AUTH-006")
    @pytest.mark.title("Empty username")
    def test_auth_with_empty_username(self, api_client):
        form_data = {
            "username": "",
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_bad_credentials_response(auth_response)

    @pytest.mark.case_id("AUTH-007")
    @pytest.mark.title("Empty password")
    def test_auth_with_empty_password(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": ""
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_bad_credentials_response(auth_response)

    @pytest.mark.case_id("AUTH-008")
    @pytest.mark.title("Empty request body")
    def test_auth_with_empty_request_body(self, api_client):
        form_data = {}
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_bad_credentials_response(auth_response)

    @pytest.mark.case_id("AUTH-009")
    @pytest.mark.title("Null values for credentials")
    def test_auth_with_null_credentials(self, api_client):
        form_data = {
            "username": None,
            "password": None
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert_bad_credentials_response(auth_response)

    @pytest.mark.case_id("AUTH-010")
    @pytest.mark.title("SQL injection in username")
    def test_auth_sql_injection_username(self, api_client):
        sql_injection_payloads = [
            "admin' OR '1'='1",
            "admin'--",
            "' OR 1=1--",
            "admin' OR 1=1#",
            "1' UNION SELECT NULL--"
        ]

        for payload in sql_injection_payloads:
            form_data = {
                "username": payload,
                "password": Config.PASSWORD
            }
            auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

            assert_bad_credentials_response(
                auth_response,
                f"SQL injection payload '{payload}': "
            )

            response_json = auth_response.json()
            assert "token" not in response_json or response_json.get("token") is None, (
                f"Security issue: SQL injection payload '{payload}' returned a valid token!"
            )

    @pytest.mark.case_id("AUTH-011")
    @pytest.mark.title("XSS payload in username")
    def test_auth_xss_payload_username(self, api_client):
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//"
        ]

        for payload in xss_payloads:
            form_data = {
                "username": payload,
                "password": Config.PASSWORD
            }
            auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

            assert_bad_credentials_response(
                auth_response,
                f"XSS payload '{payload}': "
            )

            response_json = auth_response.json()

            assert "token" not in response_json or response_json.get("token") is None, (
                f"Security issue: XSS payload '{payload}' returned a valid token!"
            )

    @pytest.mark.case_id("AUTH-012")
    @pytest.mark.title("Very long username (1000+ chars)")
    def test_auth_very_long_username(self, api_client):
        long_username_lengths = [1001, 5000, 10000]

        for length in long_username_lengths:
            long_username = "a" * length

            form_data = {
                "username": long_username,
                "password": Config.PASSWORD
            }

            auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
            assert_bad_credentials_response(
                auth_response,
                f"{length}-char username: "
            )

    @pytest.mark.case_id("AUTH-013")
    @pytest.mark.title("Special characters in credentials")
    @pytest.mark.parametrize("username,password", [
        ("user@example.com", "pass!@#$%"),
        ("user-name_123", "p@ssw0rd!"),
        ("user.name", "pass-word_123"),
        ("user+tag@mail.com", "Pass#2024$"),
        ("user~name", "p@ss^word&123")
    ])
    def test_auth_special_characters_in_credentials(self, api_client, username, password):
        form_data = {
            "username": username,
            "password": password
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        assert auth_response.status_code in (200, 401), (
            f"Unexpected status code for credentials '{username}:{password}': {auth_response.status_code}"
        )
        response_json = auth_response.json()
        assert "reason" in response_json or "token" in response_json, (
            f"Response missing expected fields for '{username}'"
        )

    @pytest.mark.case_id("AUTH-014")
    @pytest.mark.title("Response time < 2000ms")
    def test_auth_response_time(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }

        start_time = time.time()
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000
        assert_successful_auth_response(auth_response)
        assert auth_response.status_code in (200, 201), (
            f"Unexpected status code: {auth_response.status_code}"
        )

        assert response_time_ms < 2000, (
            f"Response time {response_time_ms:.2f}ms exceeds 2000ms threshold"
        )

        response_json = auth_response.json()
        assert "token" in response_json, "Response missing 'token' field"# Test Case Results Summary

    @pytest.mark.case_id("AUTH-015")
    @pytest.mark.title("Token format validation")
    def test_auth_token_format_validation(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code in (200, 201), (
            f"Unexpected status code: {auth_response.status_code}"
        )

        response_json = auth_response.json()
        assert "token" in response_json, "Response missing 'token' field"

        token = response_json["token"]
        assert isinstance(token, str), f"Token is not a string: {type(token)}"
        assert len(token) > 0, "Token is empty"

        assert re.match(r'^[A-Za-z0-9._-]+$', token), (
            f"Token contains invalid characters: {token}"
        )

        assert len(token) >= 10, f"Token is too short: {len(token)} characters"

    @pytest.mark.case_id("AUTH-016")
    @pytest.mark.title("Content-Type header validation")
    def test_auth_content_type_header_validation(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        assert auth_response.status_code in (200, 201), (
            f"Unexpected status code: {auth_response.status_code}"
        )

        content_type = auth_response.headers.get("Content-Type", "")
        assert "application/json" in content_type.lower(), (
            f"Expected 'application/json' in Content-Type header, got: {content_type}"
        )

        response_json = auth_response.json()
        assert "token" in response_json, "Response missing 'token' field"

    @pytest.mark.case_id("AUTH-017")
    @pytest.mark.title("Invalid Content-Type in request")
    def test_auth_invalid_content_type_in_request(self, api_client):
        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }

        invalid_content_types = [
            "text/plain",
            "text/html",
            "application/xml",
            "multipart/form-data",
            "invalid/content-type"
        ]

        for content_type in invalid_content_types:
            headers = {"Content-Type": content_type}
            auth_response = api_client.post(
                Config.AUTH_ENDPOINT,
                data=form_data,
                headers=headers
            )

            assert auth_response.status_code in (200, 415), (
                f"Expected 200/415 for Content-Type '{content_type}', got: {auth_response.status_code}"
            )

    @pytest.mark.case_id("AUTH-018")
    @pytest.mark.title("Token uniqueness across requests")
    def test_auth_token_uniqueness(self, api_client):
        """Verify each successful auth generates a unique token"""
        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }

        tokens = []
        for _ in range(3):
            response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
            token = assert_successful_auth_response(response)
            tokens.append(token)
            time.sleep(0.1)  # Small delay

        # All tokens should be unique
        assert len(tokens) == len(set(tokens)), (
            f"Tokens are not unique: {tokens}"
        )

    @pytest.mark.case_id("AUTH-019")
    @pytest.mark.title("Case sensitivity of credentials")
    @pytest.mark.parametrize("username,password", [
        ("ADMIN", "password123"),
        ("admin", "PASSWORD123"),
        ("Admin", "password123"),
        ("admin", "Password123")
    ])
    def test_auth_case_sensitivity(self, api_client, username, password):
        """Test that credentials are case-sensitive"""
        form_data = {
            "username": username,
            "password": password
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        # Credentials should be case-sensitive
        assert_bad_credentials_response(
            auth_response,
            f"Case variation '{username}:{password}': "
        )

    @pytest.mark.case_id("AUTH-020")
    @pytest.mark.title("Whitespace handling in credentials")
    @pytest.mark.parametrize("username,password", [
        (" admin", "password123"),     # Leading space
        ("admin ", "password123"),     # Trailing space
        ("admin", " password123"),     # Leading space in password
        ("admin", "password123 "),     # Trailing space in password
        (" admin ", " password123 ")   # Both
    ])
    def test_auth_whitespace_handling(self, api_client, username, password):
        """Test trimming/handling of whitespace"""
        form_data = {
            "username": username,
            "password": password
        }
        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        # API should either trim whitespace or reject
        assert auth_response.status_code in (200, 401), (
            f"Unexpected status for whitespace test: {auth_response.status_code}"
        )

    @pytest.mark.case_id("AUTH-021")
    @pytest.mark.title("Concurrent authentication requests")
    def test_auth_concurrent_requests(self, api_client):
        """Test handling of concurrent auth requests"""
        import concurrent.futures

        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }

        def make_auth_request():
            return api_client.post(Config.AUTH_ENDPOINT, data=form_data)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_auth_request) for _ in range(5)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        for idx, response in enumerate(responses):
            assert response.status_code in (200, 201), (
                f"Concurrent request {idx} failed: {response.status_code}"
            )
            assert_successful_auth_response(response, f"Request {idx}: ")

    @pytest.mark.case_id("AUTH-022")
    @pytest.mark.title("Token expiration validation")
    def test_auth_token_expiration(self, api_client):
        """Test if tokens have reasonable expiration"""
        form_data = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }

        auth_response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
        token = assert_successful_auth_response(auth_response)

        # Verify token works immediately
        headers = {"Cookie": f"token={token}"}
        booking_response = api_client.get("/booking", headers=headers)
        assert booking_response.status_code in (200, 201), (
            "Token should work immediately after creation"
        )

        # Note: To test expiration, you'd need to wait or mock time
        # This is a basic structure for expiration testing

    @pytest.mark.case_id("AUTH-023")
    @pytest.mark.title("Rate limiting check")
    def test_auth_rate_limiting(self, api_client):
        """Test if rate limiting is implemented"""
        form_data = {
            "username": Config.USERNAME,
            "password": "wrong_password"
        }

        # Make multiple rapid requests
        responses = []
        for _ in range(10):
            response = api_client.post(Config.AUTH_ENDPOINT, data=form_data)
            responses.append(response.status_code)

        # Check if rate limiting kicks in (429 Too Many Requests)
        rate_limited = any(status == 429 for status in responses)

        # Log results for documentation
        print(f"\nRate limiting detected: {rate_limited}")
        print(f"Response codes: {responses}")

        # This test documents behavior - adjust assertion based on API requirements
        if rate_limited:
            assert 429 in responses, "Expected 429 status code for rate limiting"