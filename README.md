# Windows Security App

A Windows security scanner and remediation toolkit that identifies common vulnerabilities on your system and walks you through fixing them one at a time.

## What It Does

### `remediate.py` — Interactive Security Hardening
Fixes common Windows security vulnerabilities. Must be run as Administrator. Every fix is interactive — it asks yes or no before making any change.

**Fixes included:**
- **Password Policy** — Enforces a minimum 12-character password length
- **Block SMB Port 445** — Adds a firewall rule to block inbound TCP 445 (WannaCry/NotPetya ransomware vector)
- **Block RPC Port 135** — Blocks inbound TCP 135 (RPC Endpoint Mapper), reduces attack surface
- **Block NetBIOS Port 139** — Blocks inbound TCP 139, a legacy protocol not needed on modern systems
- **Disable AutoRun** — Prevents Windows from auto-executing programs from USB drives or discs
- **Disable SMBv1** — Disables the obsolete SMBv1 protocol exploited by EternalBlue/WannaCry (reboot required)
- **BitLocker Guidance** — Provides step-by-step instructions for enabling full disk encryption

After running, a `remediation_log.json` is saved with a full record of what was applied, skipped, or failed.

### Supporting Modules
- **`app.py`** — Flask API with login and data endpoints
- **`commands.py`** — Discord bot commands for triggering audits and viewing reports (restricted to authorized user)
- **`daily_check.py`** — Checks for a dated report file and returns its summary
- **`inactivity_audit.py`** — Monitors for 12 hours of inactivity and triggers an automatic audit
- **`data_service.py`** — Flask blueprint for handling data input
- **`user_service.py`** — Flask blueprint for user authentication
- **`response_format.py`** — Standardized response format for audit actions

## Requirements

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

### Run the remediation script (requires Administrator)
```
Right-click your terminal -> Run as administrator
python remediate.py
```

### Run the Flask API
```bash
python app.py
```

## Notes
- `remediate.py` requires **Administrator privileges** on Windows
- SMBv1 changes require a **reboot** to fully take effect
- Save your BitLocker recovery key to your Microsoft account or a USB drive
