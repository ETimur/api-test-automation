"""Authentication API page object."""
import requests
from pages.base_page import BasePage


class LoginApiPage(BasePage):
    """Handle authentication endpoints."""

    def login(self, email: str, password: str) -> str:
        """Authenticate and return access token.
        
        Raises:
            AssertionError: If login fails
        """
        response = requests.post(
            self._url("/v1/auth/login"),
            json={"email": email, "password": password},
            timeout=15,
        )
        assert response.status_code == 200, \
            f"Login failed: {response.status_code} - {response.text}"

        data = response.json()
        token = data.get("access_token") or data.get("token")
        assert token, "No token in login response"
        return token

    def refresh_token(self, refresh_token: str) -> str:
        """Refresh an expired access token."""
        response = requests.post(
            self._url("/v1/auth/refresh"),
            json={"refresh_token": refresh_token},
            timeout=15,
        )
        assert response.status_code == 200
        return response.json()["access_token"]
