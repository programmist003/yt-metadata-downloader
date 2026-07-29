"""
URL parsing and handling utilities for YouTube.

This package provides tools for parsing and manipulating YouTube URLs.
It includes functionality to extract video IDs, handle different URL formats,
and manage URL components such as query parameters and paths.

Modules:
    - video: Contains parsers and utilities for handling YouTube video URLs.
    - url: Provides the base URL class and parsing functionality.

Key Features:
    - Parse YouTube URLs into structured components.
    - Extract video IDs from various URL formats (short, standard, embed).
    - Handle query parameters and path segments.
    - Support for wildcard imports to simplify usage.

Example Usage:
    >>> from urls import URL
    >>> url = URL.parse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    >>> print(url.query)
    {'v': ['dQw4w9WgXcQ']}
"""

# Wildcard imports for convenience
from .url import *
from .playlist import Standart as Playlist
