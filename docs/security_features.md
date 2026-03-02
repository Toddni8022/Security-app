# Security Features

## Vulnerability Scanning

- **Port scanning** — detects commonly exploited open ports (135, 139, 445, 3389)
- **SMB hardening** — flags SMBv1 usage and open SMB ports (WannaCry / NotPetya vectors)
- **Password policy** — reports when minimum password length is below 12 characters
- **AutoRun detection** — checks whether AutoRun is enabled for removable drives
- **BitLocker status** — reports drive encryption state

## Automated Remediation (`remediate.py`)

Interactive, step-by-step hardening script (requires Windows Administrator):

| Fix | Description |
|-----|-------------|
| Password length policy | Enforces ≥ 12-character minimum |
| Block SMB 445 | Adds inbound firewall rule to block ransomware vector |
| Block RPC 135 | Reduces RPC attack surface |
| Block NetBIOS 139 | Disables legacy NetBIOS |
| Disable AutoRun | Prevents USB-borne malware execution |
| Disable SMBv1 | Removes EternalBlue / WannaCry protocol support |
| BitLocker guidance | Step-by-step full-disk encryption instructions |

## Flask API Security

- API key authentication via `API_KEY` environment variable
- Input validation on all endpoints
- Structured error responses — no stack traces leaked to clients
- Logging of authentication events (without passwords)

## Reporting

Every remediation run produces a signed `remediation_log.json` with:
- Timestamp of each action
- Applied / skipped / failed status per fix
- Full detail log for audit trail
