"""Keyboard input simulation module using native Win32 APIs."""

import time
import ctypes

user32 = ctypes.windll.user32

KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

VK_CODES = {
    'enter': 0x0D,
    'return': 0x0D,
    'tab': 0x09,
    'space': 0x20,
    'backspace': 0x08,
    'escape': 0x1B,
    'esc': 0x1B,
    'shift': 0x10,
    'ctrl': 0x11,
    'control': 0x11,
    'alt': 0x12,
    'win': 0x5B,
    'windows': 0x5B,
    'left': 0x25,
    'up': 0x26,
    'right': 0x27,
    'down': 0x28,
    'delete': 0x2E,
    'del': 0x2E,
    'home': 0x24,
    'end': 0x23,
    'pageup': 0x21,
    'pagedown': 0x22,
    'f1': 0x70,
    'f2': 0x71,
    'f3': 0x72,
    'f4': 0x73,
    'f5': 0x74,
    'f6': 0x75,
    'f7': 0x76,
    'f8': 0x77,
    'f9': 0x78,
    'f10': 0x79,
    'f11': 0x7A,
    'f12': 0x7B,
}


def _get_vk(key: str) -> int:
    key_lower = key.lower()
    if key_lower in VK_CODES:
        return VK_CODES[key_lower]
    if len(key) == 1:
        # standard ASCII char
        res = user32.VkKeyScanW(ord(key))
        return res & 0xFF
    raise ValueError(f"Unknown key: {key}")


def key_down(key: str):
    vk = _get_vk(key)
    user32.keybd_event(vk, 0, KEYEVENTF_KEYDOWN, 0)


def key_up(key: str):
    vk = _get_vk(key)
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)


def press_key(key: str, delay: float = 0.05):
    """Press and release a single key."""
    key_down(key)
    time.sleep(delay)
    key_up(key)


def hotkey(*keys, delay: float = 0.05):
    """
    Execute a key combination (e.g., hotkey('ctrl', 's') or hotkey('alt', 'tab')).
    """
    for k in keys:
        key_down(k)
        time.sleep(0.02)
    time.sleep(delay)
    for k in reversed(keys):
        key_up(k)
        time.sleep(0.02)


def type_text(text: str, delay: float = 0.01):
    """Type arbitrary text character-by-character using Unicode key events."""
    for ch in text:
        # Use SendInput or keybd_event unicode flag
        user32.keybd_event(0, ord(ch), KEYEVENTF_UNICODE, 0)
        user32.keybd_event(0, ord(ch), KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0)
        if delay > 0:
            time.sleep(delay)
