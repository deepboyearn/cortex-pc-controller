"""Core control modules for Cortex PC Controller."""

from .screen import capture_screen, get_screen_resolution
from .mouse import click, move_to, drag, scroll, get_position
from .keyboard import press_key, hotkey, type_text
from .window import list_windows, find_window, focus_window

__all__ = [
    "capture_screen",
    "get_screen_resolution",
    "click",
    "move_to",
    "drag",
    "scroll",
    "get_position",
    "press_key",
    "hotkey",
    "type_text",
    "list_windows",
    "find_window",
    "focus_window",
]
