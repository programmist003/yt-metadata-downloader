from urllib.request import urlopen

def clean_url(url: str):
    """Clears URLs form redirects"""
    with urlopen(url) as response:
        url = response.geturl()
    return url

