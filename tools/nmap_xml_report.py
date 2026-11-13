#!/usr/bin/env python3
"""Summarize an Nmap XML file from an authorized assessment."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

def summarize(xml_text: str) -> dict:
    root = ET.fromstring(xml_text)
    hosts = []
    for host in root.findall("host"):
        status = host.find("status")
        addresses = [a.get("addr", "") for a in host.findall("address")]
        names = [n.get("name", "") for n in host.findall("./hostnames/hostname")]
        services = []
        for port in host.findall("./ports/port"):
            state = port.find("state")
            service = port.find("service")
            services.append({"protocol": port.get("protocol"), "port": int(port.get("portid", "0")), "state": state.get("state") if state is not None else "unknown", "service": service.get("name") if service is not None else None, "product": service.get("product") if service is not None else None, "version": service.get("version") if service is not None else None})
        hosts.append({"addresses": addresses, "hostnames": names, "status": status.get("state") if status is not None else "unknown", "services": services})
    return {"host_count": len(hosts), "hosts": hosts}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml_file", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(summarize(args.xml_file.read_text(encoding="utf-8"), indent=2))
    except (OSError, ET.ParseError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
