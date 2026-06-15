# YouTube Metadata Downloader

A Python tool for fetching YouTube video and playlist metadata using the YouTube Data API v3.

## Features

- Retrieve comprehensive metadata for YouTube videos
- Retrieve comprehensive metadata for YouTube playlists
- Fetch playlist item details (PlaylistItems)
- Output raw API responses as JSON to stdout
- Support for interactive URL input from stdin
- Automatic API key loading from `config.toml`
- Proper error handling and retry logic for failed requests

## Supported URLs

- Video URLs: `https://www.youtube.com/watch?v=VIDEO_ID`
- Playlist URLs: `https://www.youtube.com/playlist?list=PLAYLIST_ID`

## Installation

1. Clone the repository or download the files
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `config.toml` file in the project root directory with your YouTube API key:

```toml
api_key = "YOUR_YOUTUBE_API_KEY"
```

> The script loads the API key from `config.toml` when no key is provided interactively. Ensure you run the script from the project root or that `config.toml` is in your current working directory.

## Usage

### Interactive Mode (Recommended)

Run the wrapper script from the project root:

```bash
python ytmd.py
```

The script will prompt you to:
1. Enter a YouTube API key (press Enter to use the one from `config.toml`)
2. Enter video/playlist URLs (one per line, press Enter twice to finish)
3. Optionally enter playlist URLs to fetch PlaylistItems

Results are output as JSON to stdout.

### Batch Mode with File Redirection

Redirect stdin and stdout for automated processing:

```cmd
python ytmd.py < input.txt > responses.json 2> stderr.log
```

Where `input.txt` contains:
- First line: empty (to use `config.toml`) or your API key
- Following lines: YouTube URLs (one per line)
- Blank line to separate video/playlist section
- Additional playlist URLs for PlaylistItems section
- Another blank line to finish

### Output

- **stdout**: JSON array containing raw API responses for all requested resources
- **stderr**: Processing logs, prompts, and error messages

## Project Structure

- `ytmd.py` — Wrapper script to launch the main program from project root
- `src/main.py` — Main application logic
- `src/auth.py` — API key loading and authentication
- `src/config.toml` — Configuration file (optional)
- `src/kinds/` — Resource type handlers (video, playlist)
- `src/properties/` — ID extraction and data retrieval logic
- `src/type_aliases.py` — Type definitions
- `src/utils.py` — Utility functions

## API Response Format

The output is a JSON array where each element represents an API response object:

```json
[
  {
    "kind": "youtube#video",
    "id": "VIDEO_ID",
    "snippet": { ... },
    "contentDetails": { ... },
    "statistics": { ... },
    ...
  },
  {
    "kind": "youtube#playlist",
    "id": "PLAYLIST_ID",
    ...
  },
  {
    "kind": "youtube#playlistItem",
    ...
  }
]
```

## Important Notes

- Your YouTube API key must have access to YouTube Data API v3
- Be aware of API quota limits; each request consumes quota units
- Never commit your `config.toml` with actual API keys to version control
- Videos and playlists must be public or unlisted to be accessible via the API
- The tool may fail for private or deleted resources

## Error Handling

- Failed HTTP requests are retried up to 2 times with 1-second delays (for 5xx errors)
- Invalid URLs are skipped with a warning
- Duplicate URLs are filtered out
- All errors and processing information are logged to stderr
