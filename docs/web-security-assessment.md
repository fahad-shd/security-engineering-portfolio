# Web application security assessment plan

**Target:** intentionally vulnerable local application only (e.g. OWASP Juice Shop in an isolated lab).  
**Status:** plan/template; no target has been assessed by this document.

## Preparation
- Record app version, local URL, host OS, browser, and test date.
- Use a dedicated lab network and synthetic accounts.
- Configure Burp Suite Community or OWASP ZAP as an intercepting proxy.
- Keep active scanning disabled until the lab owner has confirmed the target and scope.

## Test areas (OWASP-aligned)
| Area | Safe validation focus | Defensive expectation |
|---|---|---|
| Access control | Compare access to test users' own resources; verify server-side authorization | Deny cross-user access |
| Cryptography | Inspect transport configuration and cookie flags | HTTPS; Secure, HttpOnly, appropriate SameSite |
| Injection | Use benign test inputs in the lab; inspect parameter handling | Parameterized queries and context-aware output encoding |
| Insecure design | Review workflows, rate limits, and abuse cases | Threat-modelled controls |
| Misconfiguration | Review headers, debug modes, default settings | Hardened production configuration |
| Vulnerable components | Inventory versions and compare to vendor advisories | Supported, patched dependencies |
| Authentication failures | Review password policy, MFA, reset and lockout design | Secure identity lifecycle |
| Integrity failures | Review update/deployment trust boundaries | Signed, controlled build artifacts |
| Logging/monitoring | Trigger benign test events and inspect audit trail | Useful, protected, alertable logs |
| SSRF | Review URL-fetch features using local mock endpoints only | Strict allowlists and egress controls |

## Evidence template
For each verified issue, record ID/title, date/time and lab target, preconditions and test account, non-destructive reproduction steps, expected vs observed behavior, redacted evidence, impact/likelihood, severity rationale, remediation and retest result.

## Reporting rules
Do not report scanner alerts as confirmed vulnerabilities without manual validation. Do not include exploit chains that target real systems. Label untested areas as **Not tested**, not **No issue found**.
