"""Centralized error handling for YouTube Metadata Downloader."""

from __future__ import annotations

import sys
from typing import Callable, TypeVar, Any

T = TypeVar("T")


def handle_errors(func: Callable[..., T]) -> Callable[..., T | None]:
    """Decorator to handle exceptions and log errors to stderr."""

    def wrapper(*args: Any, **kwargs: Any) -> T | None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            sys.stderr.write(f"Error in {func.__name__}: {e}\n")
            sys.stderr.flush()
            return None

    return wrapper


def log_error(message: str) -> None:
    """Log an error message to stderr."""
    sys.stderr.write(f"Error: {message}\n")
    sys.stderr.flush()


__all__ = ["handle_errors", "log_error"]