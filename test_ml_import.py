#!/usr/bin/env python3
"""Test if MLAdvancedPage can be imported without errors."""

import sys
from pathlib import Path

project_root = Path.cwd()
sys.path.insert(0, str(project_root / "01-CORE"))
sys.path.insert(0, str(project_root / "02-ML"))
sys.path.insert(0, str(project_root / "03-GUI"))

print("Testing MLAdvancedPage import...")

try:
    from gui_ml_advanced import MLAdvancedPage
    print("✅ MLAdvancedPage imported successfully!")
except Exception as e:
    print(f"❌ Error importing ML AdvancedPage: {e}")
    import traceback
    traceback.print_exc()
