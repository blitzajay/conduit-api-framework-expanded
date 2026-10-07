from __future__ import annotations

import logging
from typing import Any

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import BASE_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class BaseClient:
    """Shared HTTP transport used by all domain clients."""

    def __init__(self, token: str | None = None) -> None:
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        retry_strategy = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=0.5,
            status_forcelist=(502, 503, 504),
            allowed_methods=frozenset({"GET", "HEAD", "OPTIONS"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        if token:
            self.set_token(token)

    def set_token(self, token: str) -> None:
        self.session.headers.update({"Authorization": f"Token {token}"})

    def clear_token(self) -> None:
        self.session.headers.pop("Authorization", None)

    def close(self) -> None:
        self.session.close()

    def request(self, method: str, endpoint: str, **kwargs: Any) -> Response:
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug("%s %s", method.upper(), url)
        response = self.session.request(method=method, url=url, **kwargs)
        logger.debug("Response %s from %s", response.status_code, url)
        return response

    def get(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, json: dict | None = None, **kwargs: Any) -> Response:
        return self.request("POST", endpoint, json=json, **kwargs)

    def put(self, endpoint: str, json: dict | None = None, **kwargs: Any) -> Response:
        return self.request("PUT", endpoint, json=json, **kwargs)

    def patch(self, endpoint: str, json: dict | None = None, **kwargs: Any) -> Response:
        return self.request("PATCH", endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request("DELETE", endpoint, **kwargs)
