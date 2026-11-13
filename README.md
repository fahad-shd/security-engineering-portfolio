# Security Engineering Portfolio

Hands-on cybersecurity work focused on web application security, Python automation, network assessment, and Linux hardening.

## Projects

### Defensive automation
- [SSH authentication log analyzer](tools/log_analyzer.py) — parses Linux-style authentication events, summarizes failed and accepted logins, and flags sources over a configurable threshold.
- [Nmap XML report parser](tools/nmap_xml_report.py) — extracts hosts, ports, states, and service metadata from an authorized scan's XML output.
- [Keylogger Detection System](projects/keylogger-detection/README.md) — defensive process-metadata scanner with configurable indicators, explainable alerts, allowlisting, tests, Docker, and CI. It does not capture keystrokes.

### Machine learning and web security
- [Phishing Website Detection using ML](projects/phishing-detection/README.md) — static URL feature extraction, Random Forest training/evaluation, Flask prediction API, and dashboard. The included data is synthetic and its metrics are not real-world performance claims.
- [OWASP Juice Shop local assessment lab](labs/juice-shop/README.md) — controlled local lab setup, OWASP-aligned manual review checklist, and evidence workflow.
- [Assessment report template](labs/juice-shop/assessment-report-template.md)
- [Finding template](labs/juice-shop/finding-template.md)
- [Evidence index](labs/juice-shop/evidence/README.md)

### System and network security
- [Linux hardening checklist](docs/linux-hardening-checklist.md)
- [Methodology, authorization, and scope](docs/methodology-and-scope.md)
- [Web security assessment plan](docs/web-security-assessment.md)
- [Illustrative sample assessment report](docs/sample-assessment-report.md)

## Run the existing Python tools

Requires Python 3.10 or later.

~~~bash
python tools/log_analyzer.py data/sample_auth.log --threshold 3
python tools/nmap_xml_report.py data/sample_nmap.xml
python -m unittest discover -s tests -v
~~~

See each project README for isolated setup and test instructions. The new projects have a dedicated GitHub Actions workflow that runs tests, compilation, model training smoke checks, and Bandit static analysis.

## Safety and integrity

All included sample log, network, and phishing URL data is synthetic. The keylogger project inspects process metadata only; it does not record keystrokes or take destructive action. The phishing project does not visit submitted URLs. The Juice Shop material is a lab guide and template, not a claim that a live assessment has been completed. Test only systems you own or have explicit written authorization to assess. No Truemeds or other third-party production systems were tested for this portfolio.

## Evidence status

Code, sample data, tests, and documentation are published. Run the projects in your own environment, inspect the output, capture your own redacted screenshots, and replace any illustrative placeholders with verified observations before presenting the work as personally tested. Synthetic-data model metrics must not be described as validated production accuracy.
