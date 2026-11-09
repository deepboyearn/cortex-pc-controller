"""
Model Context Protocol (MCP) Server for Desktop Control.
Allows AI agents (Cortex CLI, Antigravity, Claude Code, Cursor) to control PC mouse, keyboard, and screen.
"""

import os
import base64
import io
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from cortex_controller.core import (
    capture_screen,
    get_screen_resolution,
    click as mouse_click,
    move_to as mouse_move,
    drag as mouse_drag,
    scroll as mouse_scroll,
    get_position as mouse_get_pos,
    press_key as kbd_press,
    hotkey as kbd_hotkey,
    type_text as kbd_type,
    list_windows as win_list,
    find_window as win_find,
    focus_window as win_focus,
)

mcp = FastMCP("cortex-pc-controller")


@mcp.tool()
def get_display_info() -> str:
    """Return primary display resolution and current cursor position."""
    w, h = get_screen_resolution()
    x, y = mouse_get_pos()
    return f"Display Resolution: {w}x{h} | Cursor Position: ({x}, {y})"


@mcp.tool()
def take_screenshot(save_path: Optional[str] = None) -> str:
    """
    Capture the current desktop screen.
    Returns the file path of the saved screenshot.
    """
    if not save_path:
        temp_dir = os.path.expanduser(r"~\.cortex_controller\screenshots")
        os.makedirs(temp_dir, exist_ok=True)
        save_path = os.path.join(temp_dir, "current_screen.png")

    capture_screen(save_path)
    return f"Screenshot successfully captured and saved to: {save_path}"


@mcp.tool()
def list_open_windows() -> str:
    """List all currently active and visible desktop windows."""
    windows = win_list()
    if not windows:
        return "No visible application windows found."
    lines = [f"- '{w['title']}' (Bounds: {w['rect']})" for w in windows[:25]]
    return "Active Windows:\n" + "\n".join(lines)


@mcp.tool()
def focus_application(window_title_keyword: str) -> str:
    """
    Bring an application window to the foreground by matching title keywords
    (e.g., 'Premiere', 'Chrome', 'Notepad').
    """
    success = win_focus(window_title_keyword)
    if success:
        return f"Successfully focused window matching '{window_title_keyword}'."
    return f"Failed to find or focus window matching '{window_title_keyword}'."


@mcp.tool()
def click(x: int, y: int, button: str = "left", clicks: int = 1) -> str:
    """
    Click at specific screen coordinates (x, y).
    button: 'left', 'right', or 'middle'.
    clicks: 1 for single click, 2 for double click.
    """
    mouse_click(x=x, y=y, button=button, clicks=clicks)
    return f"Clicked ({x}, {y}) with {button} button ({clicks} times)."


@mcp.tool()
def drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> str:
    """
    Click and drag from (start_x, start_y) to (end_x, end_y).
    Essential for dragging clips, sliders, or selecting timeline regions.
    """
    mouse_drag(start_x, start_y, end_x, end_y, duration=duration)
    return f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})."


@mcp.tool()
def scroll_wheel(delta: int) -> str:
    """Scroll mouse wheel. Positive delta scrolls up, negative scrolls down."""
    mouse_scroll(delta)
    return f"Scrolled wheel by {delta} clicks."


@mcp.tool()
def send_hotkey(keys: List[str]) -> str:
    """
    Trigger a keyboard shortcut combination (e.g. ['ctrl', 's'], ['alt', 'tab'], ['space']).
    """
    kbd_hotkey(*keys)
    return f"Executed hotkey: {'+'.join(keys)}"


@mcp.tool()
def type_string(text: str) -> str:
    """Type text into the currently active input field."""
    kbd_type(text)
    return f"Typed {len(text)} characters."


def main():
    """Run the MCP server over standard I/O."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
