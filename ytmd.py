#!/usr/bin/env python3
"""Wrapper script to launch the main project program from the repository root."""

from __future__ import annotations

import os
import sys


def main() -> int:
    project_root = os.path.dirname(__file__)
    script_path = os.path.join(project_root, "src", "main.py")
    if not os.path.exists(script_path):
        sys.stderr.write(f"Error: main script not found at {script_path}\n")
        return 1

    os.execv(sys.executable, [sys.executable, script_path, *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
