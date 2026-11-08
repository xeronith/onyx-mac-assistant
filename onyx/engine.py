"""
Onyx Inference Engine & Runtime Wrapper.
100% offline, private, zero-telemetry SLM orchestration.
"""

import os
import sys
from pathlib import Path
from typing import List, Callable, Optional, Dict, Any

# Root directories and asset paths
ROOT_DIR = Path(__file__).resolve().parent.parent

# Onyx environment variables
ONYX_MODEL_PATH = Path(os.environ.get("ONYX_MODEL_PATH", str(ROOT_DIR / "models" / "onyx-core.bin")))
ONYX_LIB_PATH = Path(os.environ.get("ONYX_LIB_PATH", str(ROOT_DIR / "models" / "libonyx.dylib")))

# Internal bridge to native SIMD engine
if ONYX_LIB_PATH.is_file():
    os.environ["CACTUS_LIB_PATH"] = str(ONYX_LIB_PATH)

# Strictly enforce 100% offline operation
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["CACTUS_TELEMETRY"] = "0"

try:
    import cactus as _backend
    tool = _backend.tool
except ImportError:
    raise RuntimeError(
        "Onyx runtime engine dependencies are missing. "
        "Please activate the virtual environment and install requirements.txt"
    )

class Onyx:
    """Onyx On-Device Agent."""

    def __init__(
        self,
        tools: Optional[List[Callable]] = None,
        weights: Optional[str] = None,
        stateless: bool = True
    ):
        self.tools = tools or []
        self.stateless = stateless

        # Resolve weights path
        if weights:
            self.weights_path = Path(weights)
        elif ONYX_MODEL_PATH.is_file():
            self.weights_path = ONYX_MODEL_PATH
        else:
            self.weights_path = None

        self._agent = _backend.Cactus(
            tools=self.tools,
            weights=str(self.weights_path) if self.weights_path else None,
            stateless=self.stateless
        )

    def run(self, query: str) -> Dict[str, Any]:
        """Execute a natural language query against registered tools."""
        return self._agent.run(query)

    def reset(self):
        """Reset conversation context."""
        if hasattr(self._agent, "reset"):
            self._agent.reset()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self._agent, "close"):
            self._agent.close()
