# Security Engineering Portfolio

Hands-on cybersecurity work focused on web application security, Python automation, network assessment, and Linux hardening.

## Projects

### Defensive automation
- [SSH authentication log analyzer](tools/log_analyzer.py) — parses Linux-style authentication events, summarizes failed and accepted logins, and flags sources over a configurable threshold.
- [Nmap XML report parser](tools/nmap_xml_report.py) — extracts hosts, ports, states, and service metadata from an authorized scan's XML output.

### Web application security
- [OWASP Juice Shop local assessment lab](labs/juice-shop/README.md) — controlled local lab setup, OWASP-aligned manual review checklist, and evidence workflow.
- [Assessment report template](labs/juice-shop/assessment-report-template.md)
- [Finding template](labs/juice-shop/finding-template.md)
- [Evidence index](labs/juice-shop/evidence/README.md)

### System and network security
- [Linux hardening checklist](docs/linux-hardening-checklist.md)
- [Methodology, authorization, and scope](docs/methodology-and-scope.md)
- [Web security assessment plan](docs/web-security-assessment.md)
- [Illustrative sample assessment report](docs/sample-assessment-report.md)

## Run the Python tools

Requires Python 3.10 or later.

~~~bash
python tools/log_analyzer.py data/sample_auth.log --threshold 3
python tools/nmap_xml_report.py data/sample_nmap.xml
python -m unittest discover -s tests -v
~~~

## Safety and integrity

All included sample log and network data is synthetic and uses documentation-only IP addresses. The Juice Shop material is a lab guide and template, not a claim that a live assessment has been completed. Test only systems you own or have explicit written authorization to assess. No Truemeds or other third-party production systems were tested for this portfolio.

## Current evidence status

The repository contains tools, sample data, checklists, and assessment templates. Run the lab yourself and replace all **Not tested** placeholders with your own verified observations and redacted evidence before describing findings as completed work.
