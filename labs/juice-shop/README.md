# OWASP Juice Shop — local web security assessment lab

**Status: lab guide and assessment worksheet only.** No Juice Shop instance has been assessed by this repository yet. Do not present the checklist as completed testing or claim findings until you run the lab and record your own evidence.

## Objective
Practice a controlled web application security review using OWASP Juice Shop, an intentionally vulnerable training application. Demonstrate a repeatable process: define scope, inspect controls, record evidence, assess risk, recommend fixes, and retest.

## Rules of engagement
- Assess only the local Juice Shop instance you start and control.
- Keep the service bound to 127.0.0.1; do not expose it to a public or shared network.
- Use synthetic accounts and data only.
- Do not send test traffic to Truemeds, public websites, or third-party infrastructure.
- Keep automated active scanning disabled for this beginner lab. Prefer manual review and passive proxy observation.
- Stop the container when finished. Do not perform denial-of-service, destructive tests, password spraying, or high-volume requests.

## Start and stop the lab
Prerequisite: Docker installed and running.

Start the container:
~~~bash
docker run --rm -d --name juice-shop -p 127.0.0.1:3000:3000 bkimminich/juice-shop
~~~

Open http://127.0.0.1:3000 in your browser. The port mapping binds the service to the local machine only.

Stop the lab:
~~~bash
docker stop juice-shop
~~~

If port 3000 is already in use, investigate the existing local service rather than exposing Juice Shop on a public interface.

## Suggested tooling
- Browser developer tools (Network, Storage/Application, and Console panels).
- OWASP ZAP or Burp Suite Community configured as a local intercepting proxy.
- A notes file for timestamps, observations, and redacted evidence.

For the first pass, observe normal browsing traffic. Do not enable active scanning. Never save session cookies, passwords, tokens, or personal data in this repository.

## Assessment workflow

### A. Establish baseline
- [ ] Record assessment date/time and local application version if available.
- [ ] Confirm the browser URL is http://127.0.0.1:3000.
- [ ] Confirm the Docker port is bound to loopback only.
- [ ] Record browser, operating system, Docker, and proxy versions.
- [ ] Create synthetic test accounts only if required.

### B. Review security controls
| Area | Safe review activity | Evidence to capture |
|---|---|---|
| Security headers | Inspect response headers during ordinary page loads | Redacted header list and response URL |
| Cookie attributes | Inspect cookies created by your own lab session | Cookie names and flags only; redact values |
| Authentication | Review sign-in, sign-out, and session behavior using your own test account | Expected/observed behavior; never capture credentials |
| Access control | Compare normal UI behavior for resources belonging to your own separate lab test accounts | Redacted request/response metadata and account roles |
| Input handling | Enter harmless boundary and punctuation characters into ordinary form fields | Field, input class, validation response |
| Error handling | Observe errors from ordinary invalid form submissions | Redacted error text and whether internals are disclosed |
| Logging | Review whether relevant security events are visible in available lab logs | Event type and timestamp |
| Dependency hygiene | Record visible application/runtime versions and research vendor advisories separately | Component, version, advisory reference |

Do not attempt to access another user's data, bypass a real account, or extract secrets. If a test unexpectedly reveals data outside your test account, stop and document only the minimum redacted evidence needed.

### C. Validate and report
1. Reproduce each potential issue once with the smallest safe test.
2. Record preconditions and expected versus observed behavior.
3. Redact credentials, tokens, personal data, and unrelated records.
4. Explain impact and likelihood; do not equate a scanner alert with a confirmed vulnerability.
5. Recommend a practical mitigation and define a retest.
6. If you cannot validate an issue, label it Unconfirmed.

## Severity rubric
Use a consistent rubric and explain your reasoning. Consider exploitability, required privileges, user interaction, scope, and confidentiality/integrity/availability impact. If using CVSS, state the version and vector. A severity label is a risk judgement, not proof that exploitation occurred.

## Evidence and completion
Use the report template, finding template, and evidence index in this folder. Name evidence files YYYYMMDD-HHMM-AREA-01.png. Capture only relevant browser panels or redacted requests. Never commit secrets, raw cookies, authorization headers, or personal information.

This lab is complete only after you perform the checks, populate the report with actual observations, attach redacted evidence you personally captured, distinguish confirmed findings from untested areas, and record remediation/retest status. Until then, keep all checks marked Not tested.
