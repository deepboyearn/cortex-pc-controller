"""Self-test verification script for Cortex PC Controller."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cortex_controller.core import get_screen_resolution, get_position, list_windows


def run_diagnostics():
    print("=" * 50)
    print("  CORTEX PC CONTROLLER - SYSTEM DIAGNOSTICS")
    print("=" * 50)

    w, h = get_screen_resolution()
    print(f"[+] Primary Display: {w} x {h}")

    cx, cy = get_position()
    print(f"[+] Current Mouse Coordinates: ({cx}, {cy})")

    windows = list_windows()
    print(f"[+] Detected {len(windows)} active window(s).")
    for win in windows[:5]:
        print(f"    - {win['title']} (Bounds: {win['rect']})")

    print("=" * 50)
    print("Diagnostics completed successfully!")


if __name__ == "__main__":
    run_diagnostics()
