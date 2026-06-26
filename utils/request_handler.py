"""HTTP request handler with logging and retry."""
import time
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


class RequestHandler:
    """Centralized HTTP request handler."""

    DEFAULT_TIMEOUT = 30

    @classmethod
    def get(cls, request_path: str, headers: dict, params: Optional[dict] = None,
            base_url: str = "", timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        url = f"{base_url}{request_path}" if base_url else request_path
        logger.info(f"GET {url} params={params}")
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        logger.info(f"Response: {response.status_code}")
        return response

    @classmethod
    def post(cls, request_path: str, headers: dict, json_data: Optional[dict] = None,
             base_url: str = "", timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        url = f"{base_url}{request_path}" if base_url else request_path
        logger.info(f"POST {url}")
        response = requests.post(url, headers=headers, json=json_data, timeout=timeout)
        logger.info(f"Response: {response.status_code}")
        return response

    @classmethod
    def put(cls, request_path: str, headers: dict, json_data: Optional[dict] = None,
            base_url: str = "", timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        url = f"{base_url}{request_path}" if base_url else request_path
        logger.info(f"PUT {url}")
        response = requests.put(url, headers=headers, json=json_data, timeout=timeout)
        logger.info(f"Response: {response.status_code}")
        return response

    @classmethod
    def patch(cls, request_path: str, headers: dict, json_data: Optional[dict] = None,
              base_url: str = "", timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        url = f"{base_url}{request_path}" if base_url else request_path
        logger.info(f"PATCH {url}")
        response = requests.patch(url, headers=headers, json=json_data, timeout=timeout)
        logger.info(f"Response: {response.status_code}")
        return response

    @classmethod
    def delete(cls, request_path: str, headers: dict,
               base_url: str = "", timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        url = f"{base_url}{request_path}" if base_url else request_path
        logger.info(f"DELETE {url}")
        response = requests.delete(url, headers=headers, timeout=timeout)
        logger.info(f"Response: {response.status_code}")
        return response
