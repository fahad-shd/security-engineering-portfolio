"""Defensive process-metadata scanner; never captures keyboard input."""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
from typing import Any
import psutil

DEFAULT_SIGNATURES = Path(__file__).with_name("signatures.json")

def load_signatures(path: str | Path = DEFAULT_SIGNATURES) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    required = {"process_names", "executable_names", "path_contains",
                "command_line_contains", "weights", "alert_threshold"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Signature file missing keys: {', '.join(sorted(missing))}")
    return data

def inspect_process(proc: Any, signatures: dict[str, Any]) -> dict[str, Any] | None:
    """Return an explainable alert record, or None when no indicator matches."""
    try:
        info = proc.as_dict(attrs=["pid", "name", "exe", "cmdline", "username"],
                            ad_value=None)
    except (psutil.NoSuchProcess, psutil.ZombieProcess):
        return None
    except psutil.AccessDenied:
        return None

    name = (info.get("name") or "").lower()
    exe = (info.get("exe") or "").lower()
    cmdline = " ".join(info.get("cmdline") or []).lower()
    path = exe.replace("\\", "/")
    weights = signatures["weights"]
    score, reasons = 0, []

    if name in {x.lower() for x in signatures["process_names"]}:
        score += int(weights["process_name"])
        reasons.append("process name matches a configured indicator")
    if Path(exe).name in {x.lower() for x in signatures["executable_names"]}:
        score += int(weights["executable_name"])
        reasons.append("executable name matches a configured indicator")
    if any(x.lower().replace("\\", "/") in path for x in signatures["path_contains"]):
        score += int(weights["path_contains"])
        reasons.append("executable path contains a configured indicator")
    if any(x.lower() in cmdline for x in signatures["command_line_contains"]):
        score += int(weights["command_line_contains"])
        reasons.append("command line contains a configured indicator")

    if score < int(signatures["alert_threshold"]):
        return None
    return {
        "pid": info.get("pid"), "name": info.get("name"),
        "executable": info.get("exe"), "username": info.get("username"),
        "score": score, "reasons": reasons,
        "severity": "high" if score >= int(signatures["alert_threshold"]) * 2 else "medium"
    }

def scan(signatures: dict[str, Any], allowlist: set[str] | None = None) -> list[dict[str, Any]]:
    allowlist = {x.lower() for x in (allowlist or set())}
    alerts = []
    for proc in psutil.process_iter():
        alert = inspect_process(proc, signatures)
        if alert and (alert.get("name") or "").lower() not in allowlist:
            alerts.append(alert)
    return sorted(alerts, key=lambda item: item["score"], reverse=True)

def main() -> None:
    parser = argparse.ArgumentParser(description="Heuristic keylogger-indicator process scanner")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="run one scan (default)")
    mode.add_argument("--watch", action="store_true", help="repeat scans")
    parser.add_argument("--interval", type=float, default=10.0)
    parser.add_argument("--signatures", default=str(DEFAULT_SIGNATURES))
    parser.add_argument("--allowlist", help="optional text file with one process name per line")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval must be greater than zero")
    signatures = load_signatures(args.signatures)
    allowlist = set()
    if args.allowlist:
        allowlist = {line.strip() for line in Path(args.allowlist).read_text().splitlines()
                     if line.strip() and not line.lstrip().startswith("#")}

    try:
        while True:
            alerts = scan(signatures, allowlist)
            if args.json:
                print(json.dumps({"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                  "alert_count": len(alerts), "alerts": alerts}))
            elif not alerts:
                print("No configured keylogger indicators detected.")
            else:
                for item in alerts:
                    print(f"[{item['severity'].upper()}] PID {item['pid']} "
                          f"{item['name']} score={item['score']}: "
                          + "; ".join(item["reasons"]))
            if not args.watch:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
