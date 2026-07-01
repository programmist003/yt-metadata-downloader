"""A module for representing and manipulating URLs (Uniform Resource Locators).

This module provides a URL class that can parse, construct, and manipulate URLs
with various components including scheme, host, port, path, query, and fragment.
"""

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, parse_qs


@dataclass
class URL:
    """A class to represent a URL with its components.

    Attributes:
        scheme (str): The scheme of the URL (e.g., 'http', 'https').
        host (str): The host or domain name (e.g., 'example.com').
        port (Optional[int]): The port number. Defaults to None.
        path (str): The path component of the URL. Defaults to '/'.
        query (Optional[str]): The query string. Defaults to None.
        fragment (Optional[str]): The fragment identifier. Defaults to None.
    """

    scheme: str
    host: str
    port: Optional[int] = None
    path: str = "/"
    query: Optional[str] = None
    fragment: Optional[str] = None

    def __str__(self) -> str:
        """Constructs the URL string from its components."""
        url = f"{self.scheme}://{self.host}"
        if self.port is not None:
            url += f":{self.port}"
        url += self.path
        if self.query is not None:
            url += f"?{self.query}"
        if self.fragment is not None:
            url += f"#{self.fragment}"
        return url

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
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL: missing scheme or host")

        # Extract host and port
        host = parsed.netloc
        port = None
        if ":" in host:
            host, port_str = host.split(":", 1)
            try:
                port = int(port_str)
            except ValueError:
                raise ValueError("Invalid port number")

        # Extract path
        path = parsed.path if parsed.path else "/"

        # Extract query
        query = parsed.query if parsed.query else None

        # Extract fragment
        fragment = parsed.fragment if parsed.fragment else None

        return cls(
            scheme=parsed.scheme,
            host=host,
            port=port,
            path=path,
            query=query,
            fragment=fragment,
        )
