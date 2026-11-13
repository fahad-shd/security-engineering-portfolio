# Methodology, authorization and scope

## Rules of engagement
- Test only assets you own or have explicit written authorization to assess.
- Define target IPs/domains, permitted dates, test accounts, rate limits, excluded systems, and emergency contacts before testing.
- Do not test Truemeds or any third-party production environment as part of this portfolio.
- Use synthetic accounts and data. Never collect real patient, customer, employee, or payment data.
- Stop if testing affects availability, exposes sensitive data, or leaves the approved scope.

## Workflow
1. **Plan:** document authorization, objectives, assets, exclusions, and success criteria.
2. **Discover:** perform low-impact asset and service identification within scope.
3. **Assess:** manually validate relevant security controls; avoid destructive payloads.
4. **Analyze:** distinguish confirmed observations from hypotheses and scanner output.
5. **Report:** assign severity with rationale, impact, evidence, and remediation.
6. **Retest:** verify fixes and record residual risk.

## Evidence handling
Redact credentials, session tokens, personal data, and sensitive host details. Store only the minimum evidence needed. Use UTC timestamps and note tool versions. Delete lab data when no longer needed.

## Finding quality
A finding should contain: title, affected component, preconditions, reproducible steps, expected vs actual behavior, impact, likelihood, severity rationale, evidence, remediation, and retest status.
