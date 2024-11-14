from googleapiclient.discovery import build
import toml
from icecream import ic


DEVELOPER_KEY = toml.load("config.toml")["api_key"]
# API client
youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
# Notice that nextPageToken now is requested in 'fields' parameter
request = youtube.search().list(
    part="id,snippet",
    type="video",
    q="Spider-Man",
    videoDuration="short",
    videoDefinition="high",
    maxResults=1,
    fields="nextPageToken,items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))",
)
response = request.execute()
ic(response)
