"""Authentication module"""
import toml
from googleapiclient.discovery import build


DEVELOPER_KEY = toml.load("config.toml")["api_key"]
# API client
youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
# https://developers.google.com/youtube/v3/docs/videos/list
