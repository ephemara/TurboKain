#!/usr/bin/env python3
"""tk — TurboKain Python driver (thin entry point).

Run from the repo root:

    python python/tk.py list
    python python/tk.py prove
    python python/tk.py run boxcar_bank --in leg.f32 --out _tmp/pulse
    python python/tk.py scan D:/data/raw/blc00_..._0000.raw --chan 60 --blocks 8

Or install nothing and call it directly; the package is stdlib-only.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make `import turbokain` work when invoked as a script (no install needed).
sys.path.insert(0, str(Path(__file__).resolve().parent))

from turbokain.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
