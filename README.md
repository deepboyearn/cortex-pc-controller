# Cortex PC Controller 🧠💻

An autonomous, production-ready AI Desktop & Application Control System designed for Windows.

Inspired by the **Cortex** architecture and the **Model Context Protocol (MCP)**, this framework enables AI assistants (such as **Cortex CLI**, **Antigravity**, **Claude Code**, or **Cursor**) to perceive, navigate, and control your PC's desktop, mouse, keyboard, and specialized desktop applications like **Adobe Premiere Pro**.

---

## 🚀 Key Features

* **🖥️ Screen Perception Engine:** High-performance Win32 GDI screen capture with automatic DPI awareness and multi-monitor support.
* **🖱️ Native Mouse Control:** Sub-pixel smooth cursor movement, single/double click, vertical scrolling, and click-and-drag (crucial for timeline scrubbing, trimming, and dragging assets).
* **⌨️ Universal Keyboard Engine:** Full Unicode character typing and multi-key shortcut combinations (`Ctrl+S`, `Alt+Tab`, `Space`, etc.).
* **🪟 Smart Window Management:** Enumerate active applications, retrieve bounding rectangles, and bring target windows (e.g., Adobe Premiere Pro, Chrome, File Explorer) directly to the foreground.
* **⚡ Native MCP (Model Context Protocol) Server:** Run as a standard `stdio` MCP server so any compliant AI agent can instantly invoke desktop tools.
* **🛠️ Direct CLI Utility:** Run direct commands from your terminal (`click`, `drag`, `hotkey`, `screenshot`, `focus`).

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│               AI Agent / LLM Brain                     │
│    (Cortex CLI / Antigravity / Claude Code / Cursor)    │
└──────────────────────────┬─────────────────────────────┘
                           │ Model Context Protocol (MCP / stdio)
┌──────────────────────────▼─────────────────────────────┐
│             Cortex PC Controller Engine                │
├─────────────┬─────────────┬─────────────┬──────────────┤
│ Screen Core │ Mouse Core  │ Keybd Core  │ Window Core  │
│ (GDI / DPI) │ (SetCursor) │ (SendInput) │ (Win32 UIA)  │
└──────┬──────┴──────┬──────┴──────┬──────┴──────┬───────┘
       │             │             │             │
┌──────▼─────────────▼─────────────▼─────────────▼───────┐
│               Windows OS Desktop Surface               │
│        (Adobe Premiere Pro, File Explorer, etc.)       │
└────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

```powershell
# Clone the repository
git clone https://github.com/deepboyearn/cortex-pc-controller.git
cd cortex-pc-controller

# Install dependencies
pip install -r requirements.txt

# (Optional) Install in editable mode for global CLI command
pip install -e .
```

---

## ⚡ Using with AI Agents (MCP Server)

To connect this controller to your AI agent (Antigravity, Cortex CLI, or Claude Desktop), add the server entry to your MCP configuration:

```json
{
  "mcpServers": {
    "cortex-pc-controller": {
      "command": "python",
      "args": [
        "-m",
        "cortex_controller.server.mcp_server"
      ]
    }
  }
}
```

Once loaded, your AI agent automatically gains the following tools:
* `take_screenshot`: Capture current screen state for vision analysis.
* `focus_application`: Bring Adobe Premiere Pro or any window into the foreground.
* `click`: Click at `(x, y)` coordinates.
* `drag`: Click and drag clips or scrub timelines.
* `send_hotkey`: Trigger shortcuts like `["ctrl", "s"]` or `["space"]`.
* `type_string`: Type titles or search queries.

---

## 💻 Direct CLI Usage

```powershell
# 1. Capture screen
python -m cortex_controller.cli screenshot --output my_desktop.png

# 2. Get display resolution and cursor position
python -m cortex_controller.cli info

# 3. Focus Adobe Premiere Pro
python -m cortex_controller.cli focus Premiere

# 4. Click at coordinates
python -m cortex_controller.cli click 960 540 --button left

# 5. Drag a clip from (500, 400) to (900, 600)
python -m cortex_controller.cli drag 500 400 900 600 --duration 0.8

# 6. Send keyboard shortcut (Save Project)
python -m cortex_controller.cli hotkey ctrl s
```

---

## 🎬 Adobe Premiere Pro Automation Example

Run the included example script to focus Premiere Pro, toggle playback, and save the project:

```powershell
python examples/premiere_pro_demo.py
```

---

## 🛡️ License

MIT License © 2026 deepboyearn
