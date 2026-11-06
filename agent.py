#!/usr/bin/env python3
"""
ONYX: On-Device macOS Assistant CLI
100% Offline • Private • Air-Gapped
"""

import sys
import time
import argparse
from pathlib import Path

# ANSI Styling
class Style:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    RESET = "\033[0m"

try:
    from onyx import Onyx, SYSTEM_TOOLS, __version__
    from onyx.engine import ONYX_MODEL_PATH
except ImportError as e:
    print(f"{Style.RED}Error loading Onyx module: {e}{Style.RESET}")
    print("Please activate the virtual environment: source .venv/bin/activate")
    sys.exit(1)

def print_banner():
    model_info = "Onyx-Core (~29 MB)"
    if ONYX_MODEL_PATH.is_file():
        size_mb = ONYX_MODEL_PATH.stat().st_size / (1024 * 1024)
        model_info = f"models/{ONYX_MODEL_PATH.name} ({size_mb:.1f} MB)"

    banner = f"""
{Style.BOLD}╔══════════════════════════════════════════════════════════════════╗
║               ⬛ ONYX: On-Device macOS Assistant                 ║
║              100% Offline • Private • Air-Gapped                 ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET}
  {Style.DIM}v{__version__} • Model: {model_info} • Apple Silicon Engine{Style.RESET}
  {Style.YELLOW}Type your commands in natural language, or 'help' / 'exit'.{Style.RESET}
"""
    print(banner)

def print_help():
    print(f"\n{Style.BOLD}Available Natural Language Capabilities:{Style.RESET}")
    print(f"  🔊 {Style.CYAN}Audio Volume:{Style.RESET}   'Set volume to 40', 'Turn it up to 80', 'What is the volume?'")
    print(f"  🌓 {Style.CYAN}Appearance:{Style.RESET}     'Turn on dark mode', 'Disable dark mode'")
    print(f"  🔋 {Style.CYAN}Battery/Power:{Style.RESET}  'What is my battery level?', 'Am I plugged in?'")
    print(f"  🔔 {Style.CYAN}Notifications:{Style.RESET}  'Show notification title Alert message Meeting starting'")
    print(f"  🚀 {Style.CYAN}App Launcher:{Style.RESET}   'Launch Notes app', 'Open Calculator', 'Launch Safari'")
    print(f"  💻 {Style.CYAN}System Specs:{Style.RESET}   'What is the system uptime?', 'Check macOS version'")
    print(f"  ℹ️  {Style.CYAN}Commands:{Style.RESET}       'help' to display this menu, 'exit' or 'quit' to exit.\n")

def process_query(agent: Onyx, query: str):
    t_start = time.time()
    response = agent.run(query)
    latency_ms = (time.time() - t_start) * 1000

    results = response.get("results") if isinstance(response, dict) else None
    reasoning = response.get("reasoning") if isinstance(response, dict) else None
    decode_tps = response.get("decode_tps") if isinstance(response, dict) else None
    peak_ram_mb = response.get("peak_ram_mb") if isinstance(response, dict) else None

    # Print results
    if results:
        for res in results:
            print(f"  {Style.GREEN}✔ {Style.BOLD}{res}{Style.RESET}")
    else:
        print(f"  {Style.YELLOW}ℹ️  {response.get('reason') or response}{Style.RESET}")

    # Print reasoning if available
    if reasoning:
        print(f"  {Style.DIM}{Style.ITALIC}🧠 Reasoning: {reasoning}{Style.RESET}")

    # Print performance stats
    perf_parts = [f"Latency: {latency_ms:.1f}ms"]
    if decode_tps:
        perf_parts.append(f"Decode: {decode_tps:.0f} tok/s")
    if peak_ram_mb:
        perf_parts.append(f"RAM: {peak_ram_mb:.1f} MB")
    perf_parts.append("100% Offline")
    print(f"  {Style.CYAN}⚡ [{' • '.join(perf_parts)}]{Style.RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Onyx On-Device macOS Assistant")
    parser.add_argument("query", nargs="*", help="Optional single query to run directly")
    parser.add_argument("--stateless", action="store_true", default=True, help="Reset context between queries")
    args = parser.parse_args()

    # Initialize Onyx agent
    agent = Onyx(tools=SYSTEM_TOOLS, stateless=args.stateless)

    # Single-shot execution if arguments were passed
    if args.query:
        query_str = " ".join(args.query)
        print(f"{Style.BOLD}{Style.BLUE}Command:{Style.RESET} {query_str}")
        process_query(agent, query_str)
        return

    # Interactive REPL mode
    print_banner()
    print(f"{Style.DIM}Initializing Onyx-Core in memory...{Style.RESET}", end="", flush=True)
    t0 = time.time()
    # Warm up engine
    agent.run("What is the volume?")
    load_time = (time.time() - t0) * 1000
    print(f" {Style.GREEN}Ready! ({load_time:.0f}ms){Style.RESET}\n")

    while True:
        try:
            user_input = input(f"{Style.BOLD}{Style.BLUE}onyx>{Style.RESET} ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "q"):
                print(f"{Style.YELLOW}Shutting down Onyx. Goodbye!{Style.RESET}")
                break

            if user_input.lower() == "help":
                print_help()
                continue

            process_query(agent, user_input)

        except KeyboardInterrupt:
            print(f"\n{Style.YELLOW}Exiting...{Style.RESET}")
            break
        except Exception as e:
            print(f"{Style.RED}Error: {e}{Style.RESET}\n")

if __name__ == "__main__":
    main()
