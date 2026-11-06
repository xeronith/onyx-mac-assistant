"""
Native macOS system tools for Onyx.
"""

import subprocess
from typing import Dict, Any, List
from onyx.engine import tool

def _run_cmd(cmd: str) -> str:
    """Helper to execute macOS system command safely."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip() or str(e)}"

# --- macOS System Tools ---

@tool
def set_system_volume(level: int) -> str:
    """Set the system output audio volume percentage (0 to 100)."""
    lvl = max(0, min(100, int(level)))
    _run_cmd(f"osascript -e 'set volume output volume {lvl}'")
    return f"Audio volume adjusted to {lvl}%"

@tool
def get_system_volume() -> str:
    """Get the current system audio volume percentage."""
    out = _run_cmd("osascript -e 'output volume of (get volume settings)'")
    return f"Current volume level is {out}%"

@tool
def set_dark_mode(enabled: bool) -> str:
    """Enable or disable macOS Dark Mode appearance."""
    state = "true" if enabled else "false"
    _run_cmd(f'osascript -e \'tell app "System Events" to tell appearance preferences to set dark mode to {state}\'')
    return f"macOS Dark Mode is now {'Enabled' if enabled else 'Disabled'}"

@tool
def get_battery_status() -> str:
    """Check the battery percentage, charge level, charging status, and power adapter."""
    raw = _run_cmd("pmset -g batt")
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    return " | ".join(lines) if lines else "Battery info unavailable"

@tool
def show_desktop_notification(title: str, message: str) -> str:
    """Display a native macOS banner alert notification."""
    t_clean = title.replace("'", "\\'")
    m_clean = message.replace("'", "\\'")
    _run_cmd(f"osascript -e 'display notification \"{m_clean}\" with title \"{t_clean}\"'")
    return f"Notification shown: [{title}] {message}"

@tool
def launch_application(app_name: str) -> str:
    """Open or launch a macOS application by name (e.g. Calculator, Notes, Safari, Terminal, Music, Calendar)."""
    clean_name = app_name.replace("'", "\\'")
    res = _run_cmd(f"open -a '{clean_name}'")
    if "Error" in res:
        return f"Failed to open '{app_name}': {res}"
    return f"Launched application '{app_name}'"

@tool
def get_system_overview() -> str:
    """Get macOS OS version release number and system uptime duration."""
    sw = _run_cmd("sw_vers -productVersion")
    uptime = _run_cmd("uptime")
    return f"macOS {sw} | Uptime: {uptime}"

SYSTEM_TOOLS: List[Any] = [
    set_system_volume,
    get_system_volume,
    set_dark_mode,
    get_battery_status,
    show_desktop_notification,
    launch_application,
    get_system_overview
]
