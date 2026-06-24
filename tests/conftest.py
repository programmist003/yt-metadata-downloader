from __future__ import annotations

import sys
from pathlib import Path

# Ensure src directory is importable when running tests from the repository root.
ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
