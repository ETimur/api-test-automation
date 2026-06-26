"""Authentication test suite."""
import allure
import pytest
from pages.login_api_page import LoginApiPage


@allure.feature("Authentication")
class TestAuthentication:
    """Auth endpoint tests."""

    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        self.login_page = LoginApiPage(base_url)

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.sanity
    def test_login_valid_credentials(self):
        """Login with valid credentials returns token."""
        import os
        token = self.login_page.login(
            os.getenv("AUTH_EMAIL", ""),
            os.getenv("AUTH_PASSWORD", ""),
        )
        assert token, "No token returned"
        assert len(token) > 10, "Token seems too short"

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.sanity
    def test_login_invalid_credentials(self):
        """Login with invalid credentials returns 401."""
        import requests
        resp = requests.post(
            f"{self.login_page.base_url}/v1/auth/login",
            json={"email": "fake@example.com", "password": "wrong"},
            timeout=15,
        )
        assert resp.status_code in [401, 403], \
            f"Expected 401/403, got {resp.status_code}"

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_email(self):
        """Login with empty email returns 400/422."""
        import requests
        resp = requests.post(
            f"{self.login_page.base_url}/v1/auth/login",
            json={"email": "", "password": "something"},
            timeout=15,
        )
        assert resp.status_code in [400, 422], \
            f"Expected 400/422, got {resp.status_code}"
