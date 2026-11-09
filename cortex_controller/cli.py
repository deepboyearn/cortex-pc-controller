"""
Command-Line Interface (CLI) for Cortex PC Controller.
Provides direct terminal commands to control PC screen, mouse, keyboard, and windows.
"""

import sys
import argparse
from cortex_controller.core import (
    capture_screen,
    get_screen_resolution,
    click,
    move_to,
    drag,
    scroll,
    get_position,
    press_key,
    hotkey,
    type_text,
    list_windows,
    focus_window,
)


def main():
    parser = argparse.ArgumentParser(
        prog="cortex-controller",
        description="Autonomous AI Desktop & Application Control System"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Screenshot
    p_screen = subparsers.add_parser("screenshot", help="Capture screen to file")
    p_screen.add_argument("--output", "-o", default="screenshot.png", help="Path to save image")

    # Resolution
    subparsers.add_parser("info", help="Get display resolution and cursor position")

    # Click
    p_click = subparsers.add_parser("click", help="Click at coordinates")
    p_click.add_argument("x", type=int, help="X coordinate")
    p_click.add_argument("y", type=int, help="Y coordinate")
    p_click.add_argument("--button", "-b", default="left", choices=["left", "right", "middle"])
    p_click.add_argument("--clicks", "-c", type=int, default=1)

    # Drag
    p_drag = subparsers.add_parser("drag", help="Click and drag between points")
    p_drag.add_argument("x1", type=int)
    p_drag.add_argument("y1", type=int)
    p_drag.add_argument("x2", type=int)
    p_drag.add_argument("y2", type=int)
    p_drag.add_argument("--duration", "-d", type=float, default=0.5)

    # Type
    p_type = subparsers.add_parser("type", help="Type text string")
    p_type.add_argument("text", type=str, help="Text to type")

    # Hotkey
    p_hotkey = subparsers.add_parser("hotkey", help="Send keyboard shortcut combination")
    p_hotkey.add_argument("keys", nargs="+", help="Keys to press (e.g. ctrl s or alt tab)")

    # Window
    p_win = subparsers.add_parser("windows", help="List all open application windows")
    p_focus = subparsers.add_parser("focus", help="Focus window by title keyword")
    p_focus.add_argument("keyword", type=str, help="Keyword in window title (e.g. Premiere)")

    # Serve MCP
    subparsers.add_parser("serve-mcp", help="Start MCP server over stdio for AI agents")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "info":
        w, h = get_screen_resolution()
        x, y = get_position()
        print(f"Screen: {w}x{h} pixels | Cursor: ({x}, {y})")

    elif args.command == "screenshot":
        capture_screen(args.output)
        print(f"Screenshot saved to: {args.output}")

    elif args.command == "click":
        click(args.x, args.y, button=args.button, clicks=args.clicks)
        print(f"Clicked ({args.x}, {args.y})")

    elif args.command == "drag":
        drag(args.x1, args.y1, args.x2, args.y2, duration=args.duration)
        print(f"Dragged from ({args.x1}, {args.y1}) to ({args.x2}, {args.y2})")

    elif args.command == "type":
        type_text(args.text)
        print(f"Typed text: {args.text}")

    elif args.command == "hotkey":
        hotkey(*args.keys)
        print(f"Sent hotkey: {'+'.join(args.keys)}")

    elif args.command == "windows":
        wins = list_windows()
        for w in wins:
            print(f"[{w['hwnd']}] {w['title']} (Bounds: {w['rect']})")

    elif args.command == "focus":
        ok = focus_window(args.keyword)
        if ok:
            print(f"Focused window matching: '{args.keyword}'")
        else:
            print(f"No window found matching: '{args.keyword}'")

    elif args.command == "serve-mcp":
        from cortex_controller.server.mcp_server import main as run_mcp
        run_mcp()


if __name__ == "__main__":
    main()
