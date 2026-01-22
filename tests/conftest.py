import pytest
from py.xml import html

from config import Config
from utils.api_client import APIClient
from utils.data_generator import generate_booking_data

@pytest.fixture(scope="module")
def ping_response(api_client):
    return api_client.get(Config.PING_ENDPOINT)

@pytest.fixture(scope="session")
def api_client():
    """Create API client instance"""
    return APIClient()


@pytest.fixture(scope="session")
def auth_token(api_client):
    """Get authentication token"""
    return api_client.get_auth_token()


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
        response = api_client.post("/booking", json=data, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            booking_id = response.json()["bookingid"]
            created_bookings.append(booking_id)
            return booking_id, data
        return None, data

    yield _create

    # Cleanup:  delete created bookings
    api_client.get_auth_token()
    for booking_id in created_bookings:
        api_client.delete(f"/booking/{booking_id}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Add custom markers to the report
    if report.when == 'call':
        case_id = item.get_closest_marker('case_id')
        title = item.get_closest_marker('title')

        if case_id:
            report.case_id = case_id.args[0] if case_id.args else 'N/A'
        if title:
            report.title = title.args[0] if title.args else 'N/A'


def pytest_html_results_table_header(cells):
    cells.insert(1, '<th>Test Case ID</th>')
    cells.insert(2, '<th>Title</th>')


def pytest_html_results_table_row(report, cells):
    case_id = getattr(report, 'case_id', 'N/A')
    title = getattr(report, 'title', 'N/A')

    cells.insert(1, f'<td>{case_id}</td>')
    cells.insert(2, f'<td>{title}</td>')