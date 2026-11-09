"""Screen capture and display management module."""

import os
import ctypes
from ctypes import wintypes
from typing import Optional, Tuple
from PIL import Image
import numpy as np

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


def set_dpi_awareness():
    """Ensure process is aware of system DPI scaling."""
    try:
        user32.SetProcessDPIAware()
    except Exception:
        pass


def get_screen_resolution() -> Tuple[int, int]:
    """Return width and height of the primary screen in pixels."""
    set_dpi_awareness()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def capture_screen(save_path: Optional[str] = None) -> Image.Image:
    """
    Capture the primary display screen using high-performance Win32 GDI.
    Returns a PIL Image object and optionally saves it to save_path.
    """
    set_dpi_awareness()
    w, h = get_screen_resolution()

    hdc_screen = user32.GetDC(0)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    hbitmap = gdi32.CreateCompatibleBitmap(hdc_screen, w, h)
    gdi32.SelectObject(hdc_mem, hbitmap)

    # BitBlt copy
    SRCCOPY = 0x00CC0020
    gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc_screen, 0, 0, SRCCOPY)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ('biSize', wintypes.DWORD),
            ('biWidth', wintypes.LONG),
            ('biHeight', wintypes.LONG),
            ('biPlanes', wintypes.WORD),
            ('biBitCount', wintypes.WORD),
            ('biCompression', wintypes.DWORD),
            ('biSizeImage', wintypes.DWORD),
            ('biXPelsPerMeter', wintypes.LONG),
            ('biYPelsPerMeter', wintypes.LONG),
            ('biClrUsed', wintypes.DWORD),
            ('biClrImportant', wintypes.DWORD)
        ]

    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = w
    bmi.biHeight = -h  # top-down orientation
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    bmi.biCompression = 0

    buf = (ctypes.c_ubyte * (w * h * 4))()
    gdi32.GetDIBits(hdc_mem, hbitmap, 0, h, buf, ctypes.byref(bmi), 0)

    # Release GDI handles
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(0, hdc_screen)

    arr = np.frombuffer(buf, dtype=np.uint8).reshape((h, w, 4))
    img = Image.fromarray(arr[:, :, [2, 1, 0]])  # Convert BGRA to RGB

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        img.save(save_path, quality=85)

    return img
