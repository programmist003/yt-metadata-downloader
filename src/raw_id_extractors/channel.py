def handle(url: URL) -> Optional[str]:
    """Parse channel handle from path."""
    m = re.match(r"^/@([^/]+)", url_obj.path)
    if m:
        return {
            "type": "channel_handle",
            "raw": str(url_obj),
            "identifier": m.group(1),
        }
    m = re.search(r"/@([^/]+)", url_obj.path)
    if m:
        return {
            "type": "channel_handle",
            "raw": str(url_obj),
            "identifier": m.group(1),
        }
    return None
