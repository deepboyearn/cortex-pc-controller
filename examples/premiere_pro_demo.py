"""
Example automation script for Adobe Premiere Pro using Cortex Controller.
Demonstrates focusing Premiere Pro, sending shortcuts, and managing timeline playback.
"""

import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cortex_controller.core import focus_window, hotkey, press_key, capture_screen


def automate_premiere():
    print("[1/4] Finding and focusing Adobe Premiere Pro...")
    focused = focus_window("Premiere")
    if not focused:
        print("[-] Premiere Pro window not detected. Please ensure Premiere Pro is open.")
        return

    print("[+] Premiere Pro brought to the foreground.")
    time.sleep(1.0)

    print("[2/4] Capturing current workspace view...")
    capture_screen("premiere_workspace.png")
    print("[+] Saved current view to 'premiere_workspace.png'.")

    print("[3/4] Triggering Timeline play/pause (Space)...")
    press_key("space")
    time.sleep(2.0)
    press_key("space")
    print("[+] Playback toggled.")

    print("[4/4] Saving Premiere Pro project (Ctrl + S)...")
    hotkey("ctrl", "s")
    print("[+] Project save command sent.")


if __name__ == "__main__":
    automate_premiere()
