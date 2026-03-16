import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class InternalServiceClient:
    """Helper class for internal service-to-service communication."""

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def post(self, endpoint, data=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        merged_headers = {}
        token = getattr(settings, "INTERNAL_SERVICE_TOKEN", "") or ""
        if token:
            merged_headers["X-Internal-Token"] = token
        if headers:
            merged_headers.update(headers)
        try:
            response = requests.post(url, json=data, headers=merged_headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling internal service {url}: {str(e)}")
            return None
