"""AUTH HELPERS"""

def assert_bad_credentials_response(response, message=""):
    """
    Helper to validate bad credentials response

    Args:
        response: API response object
        message: Optional prefix for assertion messages

    Raises:
        AssertionError: If response doesn't match expected bad credentials format
    """
    assert response.status_code in (200, 401), (
        f"{message}Expected 200/401, got: {response.status_code}"
    )

    try:
        response_json = response.json()
    except ValueError:
        raise AssertionError(f"{message}Response is not valid JSON")

    assert "reason" in response_json, (
        f"{message}Response missing 'reason' field. Got: {response_json}"
    )
    assert response_json["reason"] == "Bad credentials", (
        f"{message}Unexpected reason: {response_json['reason']}"
    )


def assert_successful_auth_response(response, message=""):
    """
    Helper to validate successful auth response

    Args:
        response: API response object
        message: Optional prefix for assertion messages

    Returns:
        str: The authentication token

    Raises:
        AssertionError: If response doesn't match expected success format
    """
    assert response.status_code in (200, 201), (
        f"{message}Unexpected status code: {response.status_code}"
    )

    try:
        response_json = response.json()
    except ValueError:
        raise AssertionError(f"{message}Response is not valid JSON")

    assert "token" in response_json, (
        f"{message}Response missing 'token' field. Got: {response_json}"
    )
    token = response_json["token"]
    assert isinstance(token, str), (
        f"{message}Token is not a string: {type(token)}"
    )
    assert len(token) > 0, f"{message}Token is empty"

    return token