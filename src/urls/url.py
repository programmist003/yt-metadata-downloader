"""A module for representing and manipulating URLs (Uniform Resource Locators).

This module provides a URL class that can parse, construct, and manipulate URLs
with various components including scheme, host, port, path, query, and fragment.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse


@dataclass
class URL:
    """A class to represent a URL with its components.

    Attributes:
        scheme (str): The scheme of the URL (e.g., 'http', 'https').
        host (str): The host or domain name (e.g., 'example.com').
        port (Optional[int]): The port number. Defaults to None.
        path (List[str]): The path component of the URL. Defaults to [].
        query (Optional[Dict[str, List[str]]]): The query dict. Defaults to None.
        fragment (Optional[str]): The fragment identifier. Defaults to None.
    """

    scheme: str
    host: str
    path: List[str]
    port: Optional[int] = None
    query: Optional[Dict[str, List[str]]] = None
    fragment: Optional[str] = None

    def __str__(self) -> str:
        """Constructs the URL string from its components."""
        path_str = "/" + "/".join(self.path) if self.path else ""
        netloc = f"{self.host}:{self.port}" if self.port is not None else self.host
        query_str = urlencode(self.query, doseq=True) if self.query else ""
        return urlunparse((
            self.scheme,
            netloc,
            path_str,
            # self.params,
            query_str,
            self.fragment
        ))


    @classmethod
    def parse(cls, url_str: str) -> "URL":
        """Parses a URL string into a URL object using urllib.parse.

        Args:
            url_str: The URL string to parse.

        Returns:
            URL: An instance of the URL class.

        Raises:
            ValueError: If the URL string is invalid.
        """
        parsed = urlparse(url_str)

        netloc = parsed.netloc
        host = netloc.split(":")[0] if netloc else ""
        port = int(netloc.split(":")[1]) if ":" in netloc else None
        path = parsed.path.strip("/").split("/") if parsed.path else []
        query = parse_qs(parsed.query, keep_blank_values=True) if parsed.query else None
        fragment = parsed.fragment if parsed.fragment else None

        return cls(
            scheme=parsed.scheme,
            host=host,
            port=port,
            path=path,
            query=query,
            fragment=fragment,
        )
