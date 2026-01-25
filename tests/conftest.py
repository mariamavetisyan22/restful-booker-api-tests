import pytest

from config import Config
from utils.api_client import APIClient
from utils.data_generator import generate_booking_data


@pytest.fixture(scope="session")
def api_client():
    """Create API client instance"""
    return APIClient()

    """PING FIXTURES"""

@pytest.fixture(scope="module")
def ping_response(api_client):
    """Get ping/health check response"""
    return api_client.get(Config.PING_ENDPOINT)

    """BOOKING FIXTURES"""

@pytest.fixture
def booking_data():
    """Generate test booking data"""
    return generate_booking_data()


@pytest.fixture
def create_booking(api_client):
    """Create a booking and return booking ID"""
    created_bookings = []

    def _create(data=None):
        if data is None:
            data = generate_booking_data()
        response = api_client.post(
            "/booking",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            booking_id = response.json()["bookingid"]
            created_bookings.append(booking_id)
            return booking_id, data
        return None, data

    yield _create

    # Cleanup: delete created bookings
    api_client.get_auth_token()
    for booking_id in created_bookings:
        api_client.delete(f"/booking/{booking_id}")