import requests
from config import Config

class APIClient:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.session = requests.Session()
        self.token = None

    def get_auth_token(self):
        """Get authentication token"""
        payload = {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        }
        response = self.post(Config.AUTH_ENDPOINT, json=payload)
        if response.status_code == 200:
            self.token = response.json().get("token")
        return self.token

    def get(self, endpoint, **kwargs):
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, timeout=Config.TIMEOUT, **kwargs)

    def post(self, endpoint, **kwargs):
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, timeout=Config.TIMEOUT, **kwargs)

    def put(self, endpoint, **kwargs):
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        if self.token:
            headers['Cookie'] = f"token={self.token}"
        kwargs['headers'] = headers
        return self.session.put(url, timeout=Config.TIMEOUT, **kwargs)

    def patch(self, endpoint, **kwargs):
        """PATCH request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        if self.token:
            headers['Cookie'] = f"token={self.token}"
        kwargs['headers'] = headers
        return self.session.patch(url, timeout=Config.TIMEOUT, **kwargs)

    def delete(self, endpoint, **kwargs):
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        if self.token:
            headers['Cookie'] = f"token={self.token}"
        kwargs['headers'] = headers
        return self.session.delete(url, timeout=Config.TIMEOUT, **kwargs)