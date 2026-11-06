# ⬛ ONYX: On-Device macOS Assistant

> An ultra-fast, 100% offline macOS assistant powered by the **Onyx-Core** on-device Small Language Model (SLM).

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20(Apple%20Silicon%20%7C%20Intel)-black.svg)](https://apple.com)
[![Offline](https://img.shields.io/badge/cloud%20dependency-0%25%20(100%25%20offline)-brightgreen.svg)]()
[![Model Size](https://img.shields.io/badge/model%20size-~29%20MB-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ONYX** translates natural language commands into typed macOS system actions and tools completely on-device. With zero cloud APIs, zero telemetry, sub-200ms latency, and a tiny memory footprint (~120 MB RAM), it turns your Mac into a private, air-gapped agentic workstation.

---

## ⚡ Performance Benchmarks

Measured on Apple Silicon (M-series, macOS):

| Metric | Measurement |
| :--- | :--- |
| **Model Size** | **~29 MB** (`models/onyx-core.bin`) |
| **Peak RAM** | **~120 MB** |
| **Inference Latency** | **~140 ms – 190 ms** |
| **Decode Throughput** | **~950 – 1,080 tokens/sec** |
| **Cloud Telemetry** | **0% (Air-gapped / 100% Offline)** |

---

## 🛠️ Built-in Capabilities

| Capability | Tool Name | Example Natural Language Prompts |
| :--- | :--- | :--- |
| 🔊 **Audio Volume** | `set_system_volume`, `get_system_volume` | *"Set volume to 40"*, *"What is the current volume?"* |
| 🔋 **Battery & Power** | `get_battery_status` | *"What is my battery level?"*, *"Am I plugged in?"* |
| 🌓 **Appearance** | `set_dark_mode` | *"Turn on dark mode"*, *"Switch to light mode"* |
| 🚀 **App Launcher** | `launch_application` | *"Launch the Notes app"*, *"Open Calculator"*, *"Launch Safari"* |
| 🔔 **Notifications** | `show_desktop_notification` | *"Show notification title 'Timer' message 'Tea is ready!'"* |
| 💻 **System Overview** | `get_system_overview` | *"What is the system uptime?"*, *"Check macOS version"* |

---

## 🚀 Installation & Quickstart

### Prerequisites
* macOS 12+ (Apple Silicon or Intel)
* Python 3.10+

### 1. Clone the Repository
```bash
git clone git@github.com:xeronith/onyx-mac-assistant.git
cd onyx-mac-assistant
```

### 2. Set Up Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
*(The native Apple Silicon engine and model weights are pre-bundled in `models/`, allowing immediate, air-gapped execution with no downloads).*

---

## 💻 Usage

### Interactive REPL Mode
Launch the interactive terminal assistant:

```bash
./run.sh
```

```text
╔══════════════════════════════════════════════════════════════════╗
║               ⬛ ONYX: On-Device macOS Assistant                 ║
║              100% Offline • Private • Air-Gapped                 ║
╚══════════════════════════════════════════════════════════════════╝
  v1.0.0 • Model: models/onyx-core.bin (33.7 MB) • Apple Silicon Engine
  Type your commands in natural language, or 'help' / 'exit'.

onyx> What is my battery level?
  ✔ Now drawing from 'AC Power' | -InternalBattery-0 80%; AC attached
  🧠 Reasoning: Battery level is 'AC Power' from result. User asked a question, so respond with that value.
  ⚡ [Latency: 144.1ms • Decode: 960 tok/s • RAM: 120.5 MB • 100% Offline]

onyx> Turn volume up to 50
  ✔ Audio volume adjusted to 50%
  🧠 Reasoning: Volume set to 50%. Confirm.
  ⚡ [Latency: 174.5ms • Decode: 964 tok/s • RAM: 120.9 MB • 100% Offline]

onyx> Launch the Calculator app
  ✔ Launched application 'Calculator'
  ⚡ [Latency: 191.7ms • Decode: 708 tok/s • RAM: 121.0 MB • 100% Offline]
```

### Single-Command Mode
Execute queries directly from your shell or automate them in workflows:

```bash
./run.sh "What is the system uptime?"
./run.sh "Turn volume down to 20"
./run.sh "Show notification title 'Build Status' message 'Compilation completed successfully'"
```

---

## 🧩 Adding Custom Tools

Onyx uses byte-level grammar constraint decoding compiled directly from standard Python function signatures. You can register custom tools using the `@tool` decorator:

```python
from onyx import Onyx, tool
import subprocess

@tool
def lock_workstation() -> str:
    """Lock the macOS screen immediately."""
    subprocess.run("pmset displaysleepnow", shell=True)
    return "Workstation locked"

# Initialize with custom tools
agent = Onyx(tools=[lock_workstation])
agent.run("Lock my screen")
```

---

## 🔒 Privacy & Offline Guarantee

The runner explicitly enforces offline execution:
```bash
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
```
All inferences execute in local memory. No audio, text queries, or metadata ever leave your machine.

---

## ⚙️ Environment Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `ONYX_MODEL_PATH` | Path to on-device `.bin` model weights | `models/onyx-core.bin` |
| `ONYX_LIB_PATH` | Path to native Apple Silicon `.dylib` engine | `models/libonyx.dylib` |
| `HF_HUB_OFFLINE` | Disables remote Hugging Face network checks | `1` (Always Offline) |

---

## 📜 License & Attribution

* Application source code is licensed under the [MIT License](LICENSE).
* Core model components and runtime are derived from Needle 3 by Cactus Compute, licensed under the [Apache License 2.0](NOTICE).
