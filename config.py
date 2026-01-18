import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = "https://restful-booker.herokuapp.com"

    # Endpoints
    PING_ENDPOINT = "/ping"
    AUTH_ENDPOINT = "/auth"
    BOOKING_ENDPOINT = "/booking"

    # Credentials
    USERNAME = os.getenv("API_USERNAME", "admin")
    PASSWORD = os.getenv("API_PASSWORD", "password123")

    # Test settings
    TIMEOUT = 10
    VERIFY_SSL = True