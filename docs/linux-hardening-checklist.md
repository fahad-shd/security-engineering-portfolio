# Linux security hardening checklist

Use on a Linux VM you administer. Record command output and system version; adapt controls to the distribution and operational requirements.

- [ ] Apply supported security updates; document patch date.
- [ ] Remove or disable unused packages, services, and listening sockets.
- [ ] Enforce least privilege; review sudoers and privileged groups.
- [ ] Prefer SSH keys; disable direct root login where operationally appropriate.
- [ ] Restrict SSH access with firewall/security-group policy.
- [ ] Use host firewall defaults-deny inbound policy with explicit required services.
- [ ] Enable automatic security updates where suitable.
- [ ] Review file permissions on sensitive configuration and secret files.
- [ ] Ensure logs are retained, access-controlled, and time-synchronized.
- [ ] Configure audit logging for privileged activity.
- [ ] Verify disk encryption and backup protection where required.
- [ ] Document service owners, exceptions, and rollback plan.

## Evidence record
| Control | Status | Evidence/command | Exception/owner |
|---|---|---|---|
| Updates | Not assessed | | |
| SSH configuration | Not assessed | | |
| Firewall | Not assessed | | |
| Privileged accounts | Not assessed | | |
| Logging | Not assessed | | |

Do not blindly apply hardening commands to production systems; validate compatibility and maintain rollback access.
