"""Window management and focus module for Windows OS."""

import ctypes
from typing import List, Dict, Optional, Tuple

user32 = ctypes.windll.user32


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long)
    ]


def list_windows() -> List[Dict[str, any]]:
    """List all open top-level application windows with titles and HWND."""
    windows = []

    def enum_cb(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                title = buf.value.strip()
                if title:
                    rect = RECT()
                    user32.GetWindowRect(hwnd, ctypes.byref(rect))
                    w = rect.right - rect.left
                    h = rect.bottom - rect.top
                    if w > 50 and h > 50:
                        windows.append({
                            "hwnd": hwnd,
                            "title": title,
                            "rect": (rect.left, rect.top, rect.right, rect.bottom),
                            "width": w,
                            "height": h
                        })
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
    return windows


def find_window(keyword: str) -> Optional[Dict[str, any]]:
    """Find the first window whose title matches keyword (case-insensitive)."""
    kw = keyword.lower()
    for win in list_windows():
        if kw in win["title"].lower():
            return win
    return None


def focus_window(keyword_or_hwnd) -> bool:
    """Bring a window to the foreground by title keyword or HWND."""
    hwnd = None
    if isinstance(keyword_or_hwnd, int):
        hwnd = keyword_or_hwnd
    else:
        win = find_window(str(keyword_or_hwnd))
        if win:
            hwnd = win["hwnd"]

    if not hwnd:
        return False

    # Restore if minimized
    SW_RESTORE = 9
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetForegroundWindow(hwnd)
    return True
