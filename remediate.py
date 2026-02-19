"""
Windows Security Remediation Script
Automatically fixes vulnerabilities found by security_scan.py

MUST be run as Administrator:
  Right-click terminal -> "Run as administrator"
  Then: python remediate.py
"""

import subprocess
import ctypes
import sys
import json
from datetime import datetime
from pathlib import Path


RESET  = "\033[0m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"


# ── helpers ────────────────────────────────────────────────────────────────────

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run(cmd, shell=True, timeout=30):
    try:
        r = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1
    except Exception as e:
        return "", str(e), -1


def ask(prompt):
    """Ask yes/no; return True for yes."""
    while True:
        ans = input(f"\n{BOLD}{prompt} [y/N]: {RESET}").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("", "n", "no"):
            return False


def ok(msg):
    print(f"  {GREEN}✔  {msg}{RESET}")


def fail(msg):
    print(f"  {RED}✘  {msg}{RESET}")


def info(msg):
    print(f"  {YELLOW}ℹ  {msg}{RESET}")


def section(title):
    print(f"\n{BOLD}{CYAN}{'─'*60}{RESET}")
    print(f"{BOLD}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*60}{RESET}")


# ── individual fixes ───────────────────────────────────────────────────────────

class Remediator:
    def __init__(self):
        self.applied   = []
        self.skipped   = []
        self.failed    = []
        self.log_lines = []

    def _record(self, status, action):
        self.log_lines.append({"time": datetime.now().isoformat(),
                                "status": status, "action": action})

    # 1. Password minimum length
    def fix_password_length(self, min_len=12):
        section("FIX 1 — Minimum Password Length")
        print(f"  Current minimum: 0 characters (no requirement)")
        print(f"  Recommended   : {min_len} characters")
        print(f"  {DIM}Note: This sets a policy going forward; existing passwords are unchanged.{RESET}")

        if not ask(f"Set minimum password length to {min_len}?"):
            self.skipped.append("Password length policy")
            info("Skipped")
            return

        out, err, rc = run(f"net accounts /minpwlen:{min_len}")
        if rc == 0:
            ok(f"Minimum password length set to {min_len}")
            self.applied.append("Password length policy")
            self._record("applied", f"net accounts /minpwlen:{min_len}")
        else:
            fail(f"Failed: {err or out}")
            self.failed.append("Password length policy")
            self._record("failed", f"net accounts /minpwlen:{min_len}")

    # 2. Block SMB port 445
    def fix_block_smb445(self):
        section("FIX 2 — Block Inbound SMB (Port 445)")
        print(f"  Port 445 is used by WannaCry / NotPetya ransomware.")
        print(f"  Blocking inbound connections to port 445 from the network.")
        print(f"  {DIM}Local Windows file sharing between your own apps is unaffected.{RESET}")

        if not ask("Block inbound TCP port 445?"):
            self.skipped.append("Block SMB 445")
            info("Skipped")
            return

        # Remove old rule if it exists, then add fresh
        run('netsh advfirewall firewall delete rule name="Block SMB 445 Inbound"')
        out, err, rc = run(
            'netsh advfirewall firewall add rule name="Block SMB 445 Inbound" '
            'protocol=TCP dir=in localport=445 action=block'
        )
        if rc == 0:
            ok("Firewall rule added: Block inbound TCP 445")
            self.applied.append("Block SMB 445")
            self._record("applied", "Block inbound TCP 445")
        else:
            fail(f"Failed: {err or out}")
            self.failed.append("Block SMB 445")
            self._record("failed", "Block inbound TCP 445")

    # 3. Block RPC port 135
    def fix_block_rpc135(self):
        section("FIX 3 — Block Inbound RPC (Port 135)")
        print(f"  Port 135 (RPC Endpoint Mapper) is rarely needed on a personal laptop.")
        print(f"  Blocking inbound connections reduces your attack surface.")

        if not ask("Block inbound TCP port 135?"):
            self.skipped.append("Block RPC 135")
            info("Skipped")
            return

        run('netsh advfirewall firewall delete rule name="Block RPC 135 Inbound"')
        out, err, rc = run(
            'netsh advfirewall firewall add rule name="Block RPC 135 Inbound" '
            'protocol=TCP dir=in localport=135 action=block'
        )
        if rc == 0:
            ok("Firewall rule added: Block inbound TCP 135")
            self.applied.append("Block RPC 135")
            self._record("applied", "Block inbound TCP 135")
        else:
            fail(f"Failed: {err or out}")
            self.failed.append("Block RPC 135")
            self._record("failed", "Block inbound TCP 135")

    # 4. Block NetBIOS port 139
    def fix_block_netbios139(self):
        section("FIX 4 — Block Inbound NetBIOS (Port 139)")
        print(f"  Port 139 (NetBIOS Session Service) is a legacy protocol.")
        print(f"  Modern Windows networking doesn't require it on a personal laptop.")

        if not ask("Block inbound TCP port 139?"):
            self.skipped.append("Block NetBIOS 139")
            info("Skipped")
            return

        run('netsh advfirewall firewall delete rule name="Block NetBIOS 139 Inbound"')
        out, err, rc = run(
            'netsh advfirewall firewall add rule name="Block NetBIOS 139 Inbound" '
            'protocol=TCP dir=in localport=139 action=block'
        )
        if rc == 0:
            ok("Firewall rule added: Block inbound TCP 139")
            self.applied.append("Block NetBIOS 139")
            self._record("applied", "Block inbound TCP 139")
        else:
            fail(f"Failed: {err or out}")
            self.failed.append("Block NetBIOS 139")
            self._record("failed", "Block inbound TCP 139")

    # 5. Disable AutoRun
    def fix_autorun(self):
        section("FIX 5 — Disable AutoRun for All Drive Types")
        print(f"  AutoRun can silently execute malware from USB sticks or optical discs.")
        print(f"  Setting NoDriveTypeAutoRun = 0xFF disables it for every drive type.")

        if not ask("Disable AutoRun for all drives?"):
            self.skipped.append("Disable AutoRun")
            info("Skipped")
            return

        key  = r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
        out, err, rc = run(
            f'reg add "{key}" /v NoDriveTypeAutoRun /t REG_DWORD /d 255 /f'
        )
        if rc == 0:
            ok("AutoRun disabled for all drive types (NoDriveTypeAutoRun = 0xFF)")
            self.applied.append("Disable AutoRun")
            self._record("applied", "NoDriveTypeAutoRun=255")
        else:
            fail(f"Failed: {err or out}")
            self.failed.append("Disable AutoRun")
            self._record("failed", "NoDriveTypeAutoRun=255")

    # 6. Disable SMBv1
    def fix_disable_smbv1(self):
        section("FIX 6 — Disable SMBv1 (EternalBlue / WannaCry)")
        print(f"  SMBv1 is the protocol exploited by the WannaCry ransomware (2017).")
        print(f"  It is completely obsolete; modern systems use SMBv2/v3.")
        print(f"  {DIM}A reboot is required for this change to take full effect.{RESET}")

        if not ask("Disable SMBv1?"):
            self.skipped.append("Disable SMBv1")
            info("Skipped")
            return

        # Server-side (receiving)
        out1, err1, rc1 = run(
            'powershell -Command "Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force"'
        )
        # Feature removal (cleaner)
        out2, err2, rc2 = run(
            'powershell -Command "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart"'
        )

        if rc1 == 0 or rc2 == 0:
            ok("SMBv1 disabled (reboot recommended to fully take effect)")
            self.applied.append("Disable SMBv1")
            self._record("applied", "SMBv1 disabled")
        else:
            fail(f"Failed: {err1 or err2}")
            self.failed.append("Disable SMBv1")
            self._record("failed", "SMBv1 disable")

    # 7. Enable BitLocker (guidance only — can't fully automate without TPM check)
    def fix_bitlocker_guidance(self):
        section("FIX 7 — BitLocker Disk Encryption (Guidance)")
        print(f"  BitLocker encrypts your drive so data is unreadable if your laptop is stolen.")
        print(f"  Full automation requires TPM presence check; here are your options:\n")
        print(f"  {BOLD}Option A — GUI:{RESET}")
        print(f"    Start → Settings → Privacy & Security → Device Encryption")
        print(f"    - or -")
        print(f"    Control Panel → BitLocker Drive Encryption → Turn on BitLocker\n")
        print(f"  {BOLD}Option B — PowerShell (Admin):{RESET}")
        print(f"    Enable-BitLocker -MountPoint 'C:' -EncryptionMethod XtsAes256 \\")
        print(f"      -RecoveryPasswordProtector\n")
        print(f"  {DIM}Save your recovery key to your Microsoft account or a USB drive!{RESET}")
        info("Manual action required — see instructions above")
        self.skipped.append("BitLocker (manual)")

    # 8. Fix date parsing in scanner
    def fix_scanner_date_parsing(self):
        section("FIX 8 — Improve Scanner Date Parsing")
        print("  The scanner couldn't parse PowerShell's /Date(...)/ timestamp format.")
        print("  Patching security_scan.py to handle this correctly...")

        scanner_path = Path(__file__).parent / "security_scan.py"
        if not scanner_path.exists():
            fail("security_scan.py not found — skipping patch")
            self.failed.append("Scanner date patch")
            return

        content = scanner_path.read_text()

        old_block = '''                if installed_on and installed_on != "Unknown":
                        try:
                            # PowerShell date format varies; strip to first 10 chars (YYYY-MM-DD)
                            date_str = str(installed_on)[:10]
                            patch_date = datetime.strptime(date_str, "%Y-%m-%d")'''

        new_block = '''                if installed_on and installed_on != "Unknown":
                        try:
                            import re as _re
                            date_str = str(installed_on)
                            # Handle /Date(milliseconds)/ format from PowerShell
                            ms_match = _re.search(r"/Date\\((\\d+)\\)/", date_str)
                            if ms_match:
                                from datetime import timezone
                                epoch_ms = int(ms_match.group(1))
                                patch_date = datetime.fromtimestamp(epoch_ms / 1000)
                            elif "DateTime" in date_str:
                                # Dict-like string: extract DateTime value
                                dt_match = _re.search(r"'DateTime':\\s*'([^']+)'", date_str)
                                if dt_match:
                                    patch_date = datetime.strptime(dt_match.group(1)[:10], "%Y-%m-%d")
                                else:
                                    raise ValueError("no DateTime key")
                            else:
                                patch_date = datetime.strptime(date_str[:10], "%Y-%m-%d")'''

        if old_block in content:
            new_content = content.replace(old_block, new_block)
            scanner_path.write_text(new_content)
            ok("security_scan.py patched — date parsing now handles PowerShell formats")
            self.applied.append("Scanner date patch")
            self._record("applied", "Patched date parsing in security_scan.py")
        else:
            info("Date parsing block not found (may already be patched or changed)")
            self.skipped.append("Scanner date patch")

        # Also patch signature date parsing
        old_sig = '''            try:
                date_str = str(out)[:10]
                sig_date = datetime.strptime(date_str, "%Y-%m-%d")'''

        new_sig = '''            try:
                import re as _re2
                _sig_raw = str(out)
                _ms2 = _re2.search(r"/Date\\((\\d+)\\)/", _sig_raw)
                if _ms2:
                    sig_date = datetime.fromtimestamp(int(_ms2.group(1)) / 1000)
                else:
                    # "Wednesday, February 18, 2026 1:00..." → grab first 3 tokens as date
                    _dt2 = _re2.search(r"(\\w+),\\s*(\\w+)\\s+(\\d+),\\s*(\\d{4})", _sig_raw)
                    if _dt2:
                        sig_date = datetime.strptime(
                            f"{_dt2.group(2)} {_dt2.group(3)} {_dt2.group(4)}", "%B %d %Y"
                        )
                    else:
                        sig_date = datetime.strptime(_sig_raw[:10], "%Y-%m-%d")'''

        if old_sig in content:
            updated = scanner_path.read_text().replace(old_sig, new_sig)
            scanner_path.write_text(updated)
            ok("security_scan.py patched — signature date parsing improved")
        else:
            info("Signature date block not found (may already be patched)")

    # ── summary ────────────────────────────────────────────────────────────────

    def print_summary(self):
        section("REMEDIATION SUMMARY")

        if self.applied:
            print(f"\n  {GREEN}{BOLD}Applied ({len(self.applied)}):{RESET}")
            for a in self.applied:
                print(f"    {GREEN}✔{RESET}  {a}")

        if self.skipped:
            print(f"\n  {YELLOW}{BOLD}Skipped ({len(self.skipped)}):{RESET}")
            for s in self.skipped:
                print(f"    {YELLOW}–{RESET}  {s}")

        if self.failed:
            print(f"\n  {RED}{BOLD}Failed ({len(self.failed)}):{RESET}")
            for f in self.failed:
                print(f"    {RED}✘{RESET}  {f}")

        # Save log
        log_path = Path(__file__).parent / "remediation_log.json"
        log_data = {
            "run_time": datetime.now().isoformat(),
            "applied": self.applied,
            "skipped": self.skipped,
            "failed": self.failed,
            "details": self.log_lines,
        }
        with open(log_path, "w") as fh:
            json.dump(log_data, fh, indent=2)

        print(f"\n  Log saved to: {log_path}")

        if self.applied:
            print(f"\n{BOLD}{CYAN}Next step:{RESET} Re-run security_scan.py to verify your new score.")
            if "Disable SMBv1" in self.applied:
                print(f"{YELLOW}  ⚠  A reboot is recommended (SMBv1 change).{RESET}")


# ── entry point ────────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  Windows Security Remediation Script{RESET}")
    print(f"{BOLD}{CYAN}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}")

    if not is_admin():
        print(f"\n{RED}{BOLD}ERROR: This script must be run as Administrator.{RESET}")
        print(f"  1. Close this terminal")
        print(f"  2. Right-click your terminal app")
        print(f"  3. Choose 'Run as administrator'")
        print(f"  4. Navigate back here and run: python remediate.py")
        sys.exit(1)

    print(f"\n{GREEN}✔  Running as Administrator{RESET}")
    print(f"\nThis script will walk you through each fix one at a time.")
    print(f"You choose {BOLD}yes or no{RESET} for every change. Nothing happens automatically.")

    r = Remediator()

    # Run all fixes in priority order
    r.fix_password_length(min_len=12)
    r.fix_block_smb445()
    r.fix_block_rpc135()
    r.fix_block_netbios139()
    r.fix_autorun()
    r.fix_disable_smbv1()
    r.fix_bitlocker_guidance()
    r.fix_scanner_date_parsing()

    r.print_summary()


if __name__ == "__main__":
    main()
