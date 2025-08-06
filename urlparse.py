"""URL parser module"""

from urllib.request import urlopen

from furl import furl


def clean_url(url: str):
    """Clears URLs form redirects"""
    with urlopen(url) as response:
        url = response.geturl()
    return url


def check_domain(url: str) -> bool:
    """Check if the URL is a YouTube URL"""
    host = furl(url).host
    return host in ("youtube.com", "www.youtube.com", "youtu.be")
