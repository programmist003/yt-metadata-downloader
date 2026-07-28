from typing import Optional

from ..url import URL


def short(url_obj: URL) -> Optional[str]:
    """Parse short YouTube URL (youtu.be)."""
    vid = url_obj.path[0]
    if vid and url_obj.host == "youtu.be":
        return vid
    return None


def query(url_obj: URL) -> Optional[str]:
    """Parse video ID from query parameters."""
    query_params = url_obj.query
    if query_params and "v" in query_params and query_params["v"]:
        return query_params["v"][0]
    return None


def embed(url_obj: URL) -> Optional[str]:
    """Parse video ID from embed path."""
    m = re.match(r"^/embed/([^/]+)", url_obj.path)
    if m:
        return m.group(1)
    return None


if __name__ == "__main__":
    print(
        "https://youtu.be/mtpEUZTdeNY?si=FXUSjGxMjMC3cIyq",
        "->",
        short(URL.parse("https://youtu.be/mtpEUZTdeNY?si=FXUSjGxMjMC3cIyq")),
    )
    pass
