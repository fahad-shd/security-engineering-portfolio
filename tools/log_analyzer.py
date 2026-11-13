#!/usr/bin/env python3
"""Analyze Linux-style authentication logs for defensive triage."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
import sys

FAILED = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>[0-9a-fA-F:.]+)")
ACCEPTED = re.compile(r"Accepted (?:password|publickey) for (?P<user>\S+) from (?P<ip>[0-9a-fA-F:.]+)")
INVALID = re.compile(r"Invalid user (?P<user>\S+) from (?P<ip>[0-9a-fA-F:.]+)")

@dataclass
class Event:
    line: int
    kind: str
    user: str
    source: str

def parse_line(line: str, number: int) -> Event | None:
    for pattern, kind in ((FAILED, "failed"), (ACCEPTED, "accepted"), (INVALID, "invalid_user")):
        match = pattern.search(line)
        if match:
            return Event(number, kind, match.group("user"), match.group("ip"))
    return None

def analyze(lines: list[str], threshold: int = 5) -> dict:
    events = [event for i, line in enumerate(lines, 1) if (event := parse_line(line, i))]
    failed_by_ip = Counter(e.source for e in events if e.kind in {"failed", "invalid_user"})
    failed_by_user = Counter(e.user for e in events if e.kind in {"failed", "invalid_user"})
    accepted_by_ip = Counter(e.source for e in events if e.kind == "accepted")
    success_after_failures = []
    seen_failed = defaultdict(int)
    for event in events:
        if event.kind in {"failed", "invalid_user"}:
            seen_failed[(event.source, event.user)] += 1
        elif event.kind == "accepted" and seen_failed[(event.source, event.user)]:
            success_after_failures.append({"source": event.source, "user": event.user, "prior_failures_in_file": seen_failed[(event.source, event.user)], "line": event.line})
    return {"parsed_events": len(events), "failed_attempts_by_source": dict(failed_by_ip), "failed_attempts_by_user": dict(failed_by_user), "accepted_logins_by_source": dict(accepted_by_ip), "sources_over_threshold": sorted(ip for ip, count in failed_by_ip.items() if count >= threshold), "success_after_failures": success_after_failures, "unparsed_lines": len(lines) - len(events)}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logfile", type=Path)
    parser.add_argument("--threshold", type=int, default=5)
    args = parser.parse_args()
    if args.threshold < 1:
        parser.error("--threshold must be >= 1")
    try:
        report = analyze(args.logfile.read_text(encoding="utf-8", errors="replace").splitlines(), args.threshold)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    import json
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
