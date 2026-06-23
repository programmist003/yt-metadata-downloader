# YouTube Metadata Downloader

Small Python utility to fetch raw YouTube Data API v3 responses for videos, playlists and playlist items.

**Recommended (Windows):** use the provided wrapper `ytmd.bat` from the project root.

Quick start (Windows):

```cmd
ytmd.bat < input.txt > responses.json 2> stderr.log
```

Quick start (any platform):

```bash
python src/main.py < input.txt > responses.json 2> stderr.log
```

How it works
- Prompts and status messages are written to `stderr`.
- The program reads URLs and optional API key from `stdin` (see modes below).
- Raw API responses (JSON array) are written to `stdout` (UTF-8).

Modes of operation
- Interactive mode (recommended for ad-hoc use): run `ytmd.bat` (Windows) or `python src/main.py` without redirecting `stdin`. The program will prompt for an API key (press Enter to use `config.toml`), then repeatedly ask for resource URLs. Enter one URL per line; an empty line finishes the current section. After the first section you can optionally enter playlist URLs to fetch `playlistItems`.

- Batch mode (non-interactive): provide an `input.txt` via stdin. The format is:

  - First line: empty to use `config.toml` or your API key on the first line.
  - Next lines: resource URLs (video or playlist), one per line.
  - Blank line: separates the primary resource section from the playlist-items section.
  - After the blank line: playlist URLs (one per line) for which `playlistItems` will be fetched.
  - EOF or another blank line: end input.

Examples

- Interactive (Windows):

  ```cmd
  ytmd.bat
  ```

  Then follow prompts: enter API key or press Enter to use `config.toml`, enter URLs, finish with an empty line.

- Batch example with `input.txt`:

  ```text

  https://www.youtube.com/watch?v=dQw4w9WgXcQ
  https://www.youtube.com/watch?v=lp-EO5I60KA

  https://www.youtube.com/playlist?list=PL...   # playlistItems fetch

  ```

Security and config
- Put your API key in `config.toml` if you want to avoid typing it interactively. Do not commit `config.toml` with secrets to version control.

Notes and behavior
- Invalid or unsupported URLs are ignored and reported on `stderr`.
- Duplicate URLs are ignored.
- The tool retries transient HTTP errors a few times before giving up.

Useful files
- [ytmd.bat](ytmd.bat) — Windows wrapper (recommended for Windows users)
- [src/main.py](src/main.py) — cross-platform entrypoint and interactive logic

If you want, I can also add a short example `input.txt` file to the repo.
