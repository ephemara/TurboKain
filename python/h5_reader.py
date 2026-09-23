#!/usr/bin/env python3
"""CLI entry point for h5_reader."""
import sys
from pathlib import Path

# Ensure turbokain is on path
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from turbokain.h5_reader import main

if __name__ == "__main__":
    sys.exit(main())
