# YouTube Metadata Downloader

Small Python tool to fetch YouTube video and playlist metadata (YouTube Data API v3).

Primary scenario (Windows): use the provided batch wrapper `ytmd.bat` from the project root.

Usage (Windows — recommended):

```cmd
ytmd.bat < input.txt > responses.json 2> stderr.log
```

Primary behavior:
- Reads prompts from stderr and URLs from stdin according to the `input.txt` layout (see below).
- Writes a JSON array of raw API responses to stdout (`response.json` in the example).

Alternative (other platforms): run the Python entrypoint `src/main.py` directly.

Usage (Linux / macOS / any platform with Python):

```bash
python src/main.py < input.txt > response.json 2> stderr.log
```

Input file format (`input.txt`):
- First line: empty to use `config.toml` or your YouTube API key.
- Following lines: YouTube URLs (one per line) for videos and playlists.
- A blank line separates the first resource section from the playlist-items section.
- After the blank line: playlist URLs (one per line) to fetch `playlistItems`.
- An empty line (or EOF) finishes input.

Quick examples:

- Use `config.toml` API key and fetch two videos:

```cmd
ytmd.bat < input.txt > out.json
```

Where `input.txt` could be:

```

https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=lp-EO5I60KA


```

Notes and tips:
- Ensure `python` is available in PATH on Windows for `ytmd.bat`.
- `ytmd.bat` is the primary, user-facing entrypoint for Windows users; `src/main.py` is the cross-platform entrypoint.
- Validate JSON with Python: `python -m json.tool response.json > nul && echo JSON_OK` (Windows) or `> /dev/null` on Unix.
- Keep your `config.toml` out of version control.

Project layout (important files):
- `ytmd.bat` — Windows wrapper (preferred on Windows)
- `run_main.bat` — wrapper that runs `src/main.py` and forwards args
- `src/main.py` — main application logic (cross-platform entrypoint)
- `src/auth.py`, `src/kinds/`, `src/properties/` — internal modules

More details and examples are available in the repository.
