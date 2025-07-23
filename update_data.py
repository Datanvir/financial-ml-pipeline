#!/usr/bin/env python3
"""
Convenience script to update BTC data from the root directory.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from data_collection.daily_updater import main

if __name__ == "__main__":
    main()
