"""Global pytest fixtures for API tests."""
import os
import pytest
from dotenv import load_dotenv
from pages.login_api_page import LoginApiPage
from utils.request_handler import RequestHandler

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://api.staging.healthnote.example.com")


@pytest.fixture(scope="session")
def auth_headers(base_url):
    """Authenticate and return headers with token."""
    login_page = LoginApiPage(base_url)
    token = login_page.login(
        email=os.getenv("AUTH_EMAIL", ""),
        password=os.getenv("AUTH_PASSWORD", ""),
    )
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


@pytest.fixture(scope="session")
def facility_id():
    return os.getenv("FACILITY_ID", "test-facility-001")


@pytest.fixture(scope="session")
def provider_id():
    return os.getenv("PROVIDER_ID", "test-provider-001")
