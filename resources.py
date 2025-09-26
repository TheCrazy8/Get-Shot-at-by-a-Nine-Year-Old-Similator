"""Resource helper utilities for locating assets in dev and PyInstaller builds."""
from __future__ import annotations
import os, sys
from pathlib import Path

_BASE = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

def resource_path(relative: str) -> str:
    """Return absolute path for a bundled resource (icon, music, lore, etc.)."""
    return str(_BASE / relative)

# Optional: safe mixer init wrapper (not yet widely used; placeholder for future refactor)

def safe_init_mixer(pygame):  # pass pygame module to avoid import here if unavailable
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        return True
    except Exception:
        return False
