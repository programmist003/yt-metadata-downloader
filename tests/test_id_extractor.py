import json

from types import SimpleNamespace

import pytest

from src.links.parser import parse_url
from src.links import id_extractor


class DummyResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return self._json


def test_resolve_channel_id_for_handle(monkeypatch):
    # simulate API returning a channel id for handle
    def fake_get(url, params=None, timeout=None, headers=None):
        assert params is not None
        assert "forHandle" in params
        return DummyResponse(json_data={"items": [{"id": "UC_HANDLE_ID"}]})

    monkeypatch.setattr(id_extractor.requests, "get", fake_get)

    parsed = parse_url("https://www.youtube.com/@SomeHandle")
    cid = id_extractor.resolve_channel_id(parsed, api_key="DUMMY")
    assert cid == "UC_HANDLE_ID"


def test_resolve_channel_id_for_username(monkeypatch):
    def fake_get(url, params=None, timeout=None, headers=None):
        assert "forUsername" in params
        return DummyResponse(json_data={"items": [{"id": "UC_CUSTOM_ID"}]})

    monkeypatch.setattr(id_extractor.requests, "get", fake_get)

    parsed = parse_url("https://www.youtube.com/c/CustomName")
    cid = id_extractor.resolve_channel_id(parsed, api_key="DUMMY")
    assert cid == "UC_CUSTOM_ID"


def test_resolve_channel_id_not_found(monkeypatch):
    def fake_get(url, params=None, timeout=None, headers=None):
        return DummyResponse(json_data={"items": []})

    monkeypatch.setattr(id_extractor.requests, "get", fake_get)

    parsed = parse_url("https://www.youtube.com/@NotExist")
    cid = id_extractor.resolve_channel_id(parsed, api_key="DUMMY")
    assert cid is None
