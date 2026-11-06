"""
Onyx: On-Device, Air-Gapped macOS Assistant.
Powered by an ultra-fast, local SLM with deterministic tool execution.
"""

__version__ = "1.0.0"

from onyx.engine import Onyx, tool
from onyx.tools import SYSTEM_TOOLS

__all__ = ["Onyx", "tool", "SYSTEM_TOOLS", "__version__"]
