"""Small HTTP client wrapper around `requests` with retries and JSON helper."""

from __future__ import annotations

from typing import Optional, Dict
import sys

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient:
    def __init__(
        self,
        verify: bool = True,
        retries: int = 3,
        backoff: float = 1.0,
        timeout: int = 30,
    ):
        self.session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.verify = verify
        self.timeout = timeout

    def get_json(
        self, url: str, params: Dict | None = None, headers: Dict | None = None
    ) -> Optional[Dict]:
        try:
            hdrs = {"User-Agent": "yt-metadata-downloader/1.0"}
            if headers:
                hdrs.update(headers)
            resp = self.session.get(
                url,
                params=params,
                timeout=self.timeout,
                headers=hdrs,
                verify=self.verify,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            sys.stderr.write(f"HTTP request failed: {e}\n")
            sys.stderr.flush()
            return None


__all__ = ["HttpClient"]
