"""Mouse input simulation module using native Win32 APIs."""

import time
import ctypes
from typing import Tuple

user32 = ctypes.windll.user32

# Win32 Mouse Event Flags
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_ABSOLUTE = 0x8000


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_position() -> Tuple[int, int]:
    """Get current cursor position (x, y)."""
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return int(pt.x), int(pt.y)


def move_to(x: int, y: int, smooth: bool = False, duration: float = 0.2):
    """Move mouse cursor to (x, y). Optionally animate smoothly."""
    if not smooth:
        user32.SetCursorPos(int(x), int(y))
        return

    start_x, start_y = get_position()
    steps = int(max(10, duration * 60))
    delay = duration / steps
    for step in range(1, steps + 1):
        t = step / steps
        # Smooth ease-in-out
        ease = t * t * (3 - 2 * t)
        curr_x = int(start_x + (x - start_x) * ease)
        curr_y = int(start_y + (y - start_y) * ease)
        user32.SetCursorPos(curr_x, curr_y)
        time.sleep(delay)
    user32.SetCursorPos(int(x), int(y))


def click(x: int = None, y: int = None, button: str = "left", clicks: int = 1, interval: float = 0.05):
    """Click at (x, y) or current location."""
    if x is not None and y is not None:
        move_to(x, y)

    btn = button.lower()
    down_flag = MOUSEEVENTF_LEFTDOWN if btn == "left" else (MOUSEEVENTF_RIGHTDOWN if btn == "right" else MOUSEEVENTF_MIDDLEDOWN)
    up_flag = MOUSEEVENTF_LEFTUP if btn == "left" else (MOUSEEVENTF_RIGHTUP if btn == "right" else MOUSEEVENTF_MIDDLEUP)

    for i in range(clicks):
        user32.mouse_event(down_flag, 0, 0, 0, 0)
        time.sleep(interval)
        user32.mouse_event(up_flag, 0, 0, 0, 0)
        if i < clicks - 1:
            time.sleep(interval)


def drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5):
    """Click and drag from (start_x, start_y) to (end_x, end_y). Useful for Premiere timelines & sliders."""
    move_to(start_x, start_y)
    time.sleep(0.05)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    move_to(end_x, end_y, smooth=True, duration=duration)
    time.sleep(0.05)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def scroll(delta: int):
    """Scroll mouse wheel vertically. Positive is up, negative is down."""
    user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, int(delta * 120), 0)
