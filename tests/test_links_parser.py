import pytest

from links.parser import parse_url, is_video_url, is_playlist_url


@pytest.mark.parametrize(
    "url,expected_type,expected_id",
    [
        (
            "https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw",
            "channel_id",
            "UC_x5XG1OV2P6uZZ5FSM9Ttw",
        ),
        ("https://www.youtube.com/c/SomeChannel", "channel_custom", "SomeChannel"),
        ("https://www.youtube.com/@SomeHandle", "channel_handle", "SomeHandle"),
        ("https://youtu.be/VIDEO123", "video", "VIDEO123"),
        ("https://www.youtube.com/watch?v=VIDABC", "video", "VIDABC"),
        ("https://www.youtube.com/playlist?list=PL12345", "playlist", "PL12345"),
        ("https://example.com/", "other", None),
    ],
)
def test_parse_url(url, expected_type, expected_id):
    info = parse_url(url)
    assert info["type"] == expected_type
    assert info["identifier"] == expected_id


def test_helpers():
    assert is_video_url("https://youtu.be/VID1")
    assert is_playlist_url("https://www.youtube.com/playlist?list=PL1")
