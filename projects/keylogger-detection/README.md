# Keylogger Detection System

A defensive Python process-monitoring prototype that flags processes matching a transparent, editable set of suspicious indicators. It uses `psutil` to inspect process metadata (name, executable path, and command-line text); it **does not capture keystrokes, install hooks, terminate processes, or perform persistence**.

## Detection approach
- Exact process-name and executable-name indicators.
- Suspicious path fragments and command-line indicators.
- Weighted indicator scoring with explainable reasons.
- Optional allowlist, JSON output, one-shot scan, and periodic monitoring.
- Permission-denied and exited-process cases are handled without crashing.

This is a heuristic triage aid, not an antivirus product. A matching name or command-line token is not proof of malicious activity; validate alerts with process ownership, parent process, file hash, signature, and endpoint telemetry.

## Run locally
Python 3.10+.

```bash
python -m venv .venv
# activate the environment, then:
pip install -r requirements.txt
python detector.py --once
python detector.py --watch --interval 5 --json
python detector.py --once --signatures signatures.json --allowlist allowlist.txt
```

The default signature file is deliberately small and illustrative. Tune it for the environment and document the rationale for each indicator. Use only on systems you own or are authorized to monitor.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Limitations
Process metadata alone cannot reliably establish keylogging. Legitimate remote-support, accessibility, automation, and developer tools can produce false positives; stealthy malware can evade these indicators. The project reports evidence for human triage rather than making destructive decisions.