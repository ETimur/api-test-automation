"""Base API page object."""
from utils.request_handler import RequestHandler


class BasePage:
    """Base class for API page objects."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.request = RequestHandler

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"
