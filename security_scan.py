"""
Windows Security Vulnerability Scanner
Checks common security issues on a Windows laptop.
Run with: python security_scan.py
"""

import subprocess
import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path


RESET = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def run_cmd(cmd, shell=True, timeout=15):
    try:
        result = subprocess.run(
            cmd, shell=shell, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1
    except Exception as e:
        return "", str(e), -1


class SecurityScanner:
    def __init__(self):
        self.findings = []
        self.passed = []
        self.warnings = []

    def add_finding(self, severity, category, title, detail):
        entry = {"severity": severity, "category": category, "title": title, "detail": detail}
        if severity == "CRITICAL" or severity == "HIGH":
            self.findings.append(entry)
        elif severity == "MEDIUM" or severity == "LOW":
            self.warnings.append(entry)
        else:
            self.passed.append(entry)

    def print_header(self):
        print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
        print(f"{BOLD}{CYAN}  Windows Security Vulnerability Scanner{RESET}")
        print(f"{BOLD}{CYAN}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
        print(f"{BOLD}{CYAN}{'='*60}{RESET}\n")

    def print_section(self, name):
        print(f"\n{BOLD}[ {name} ]{RESET}")
        print("-" * 50)

    # ------------------------------------------------------------------ #
    #  1. Windows Update / Patch Status
    # ------------------------------------------------------------------ #
    def check_windows_update(self):
        self.print_section("Windows Update Status")

        out, _, rc = run_cmd(
            'powershell -Command "Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5 | ConvertTo-Json"'
        )
        if out:
            try:
                patches = json.loads(out) if out.startswith("[") else [json.loads(out)]
                latest = patches[0]
                installed_on = latest.get("InstalledOn", "Unknown")
                print(f"  Last patch: {latest.get('HotFixID')} installed {installed_on}")

                # Try to parse date
                if installed_on and installed_on != "Unknown":
                    try:
                        # PowerShell date format varies; strip to first 10 chars (YYYY-MM-DD)
                        date_str = str(installed_on)[:10]
                        patch_date = datetime.strptime(date_str, "%Y-%m-%d")
                        days_old = (datetime.now() - patch_date).days
                        if days_old > 60:
                            self.add_finding("HIGH", "Updates", "System patches are out of date",
                                             f"Last patch installed {days_old} days ago")
                            print(f"  {RED}FAIL{RESET}: Last patch is {days_old} days old (>60 days)")
                        elif days_old > 30:
                            self.add_finding("MEDIUM", "Updates", "System patches may be stale",
                                             f"Last patch installed {days_old} days ago")
                            print(f"  {YELLOW}WARN{RESET}: Last patch is {days_old} days old")
                        else:
                            self.add_finding("PASS", "Updates", "System is recently patched", "")
                            print(f"  {GREEN}PASS{RESET}: Patched {days_old} days ago")
                    except Exception:
                        print(f"  {YELLOW}INFO{RESET}: Could not parse patch date")
            except Exception:
                print(f"  {YELLOW}INFO{RESET}: Could not parse hotfix data")
        else:
            print(f"  {YELLOW}WARN{RESET}: Could not retrieve update information")

    # ------------------------------------------------------------------ #
    #  2. Windows Defender / Antivirus
    # ------------------------------------------------------------------ #
    def check_antivirus(self):
        self.print_section("Antivirus / Windows Defender")

        # Real-time protection
        out, _, _ = run_cmd(
            'powershell -Command "(Get-MpComputerStatus).RealTimeProtectionEnabled"'
        )
        if out.strip().lower() == "true":
            self.add_finding("PASS", "Antivirus", "Real-time protection enabled", "")
            print(f"  {GREEN}PASS{RESET}: Real-time protection is ON")
        else:
            self.add_finding("CRITICAL", "Antivirus", "Real-time protection is DISABLED",
                             "Windows Defender real-time protection is turned off")
            print(f"  {RED}CRITICAL{RESET}: Real-time protection is DISABLED")

        # Signature age
        out, _, _ = run_cmd(
            'powershell -Command "(Get-MpComputerStatus).AntivirusSignatureLastUpdated"'
        )
        if out:
            try:
                date_str = str(out)[:10]
                sig_date = datetime.strptime(date_str, "%Y-%m-%d")
                days_old = (datetime.now() - sig_date).days
                if days_old > 7:
                    self.add_finding("HIGH", "Antivirus", "Antivirus signatures are outdated",
                                     f"Signatures are {days_old} days old")
                    print(f"  {RED}FAIL{RESET}: Signatures are {days_old} days old")
                else:
                    self.add_finding("PASS", "Antivirus", "Antivirus signatures are current", "")
                    print(f"  {GREEN}PASS{RESET}: Signatures updated {days_old} days ago")
            except Exception:
                print(f"  {YELLOW}INFO{RESET}: Could not parse signature date: {out[:30]}")

    # ------------------------------------------------------------------ #
    #  3. Firewall
    # ------------------------------------------------------------------ #
    def check_firewall(self):
        self.print_section("Firewall Status")

        for profile in ["Domain", "Private", "Public"]:
            out, _, _ = run_cmd(
                f'powershell -Command "(Get-NetFirewallProfile -Name {profile}).Enabled"'
            )
            enabled = out.strip().lower() == "true"
            status = f"{GREEN}ON{RESET}" if enabled else f"{RED}OFF{RESET}"
            print(f"  {profile:10}: {status}")
            if not enabled:
                self.add_finding("HIGH", "Firewall", f"{profile} firewall profile is disabled",
                                 f"The {profile} firewall profile is turned off")
            else:
                self.add_finding("PASS", "Firewall", f"{profile} firewall is enabled", "")

    # ------------------------------------------------------------------ #
    #  4. User Account Control (UAC)
    # ------------------------------------------------------------------ #
    def check_uac(self):
        self.print_section("User Account Control (UAC)")

        out, _, _ = run_cmd(
            r'reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA'
        )
        if "0x1" in out:
            self.add_finding("PASS", "UAC", "UAC is enabled", "")
            print(f"  {GREEN}PASS{RESET}: UAC is enabled")
        elif "0x0" in out:
            self.add_finding("CRITICAL", "UAC", "UAC is DISABLED",
                             "User Account Control is turned off, increasing risk of privilege escalation")
            print(f"  {RED}CRITICAL{RESET}: UAC is DISABLED")
        else:
            print(f"  {YELLOW}INFO{RESET}: Could not determine UAC status")

    # ------------------------------------------------------------------ #
    #  5. BitLocker / Drive Encryption
    # ------------------------------------------------------------------ #
    def check_bitlocker(self):
        self.print_section("Disk Encryption (BitLocker)")

        out, _, _ = run_cmd(
            'powershell -Command "Get-BitLockerVolume -MountPoint C: | Select-Object ProtectionStatus | ConvertTo-Json"'
        )
        if out:
            try:
                data = json.loads(out)
                status = data.get("ProtectionStatus", "Unknown")
                # 1 = On, 0 = Off
                if str(status) == "1":
                    self.add_finding("PASS", "Encryption", "C: drive is BitLocker encrypted", "")
                    print(f"  {GREEN}PASS{RESET}: C: drive is encrypted (BitLocker On)")
                else:
                    self.add_finding("HIGH", "Encryption", "C: drive is NOT encrypted",
                                     "BitLocker is off; data at rest is unprotected if device is lost/stolen")
                    print(f"  {RED}FAIL{RESET}: C: drive is NOT encrypted (BitLocker Off)")
            except Exception:
                print(f"  {YELLOW}INFO{RESET}: Could not parse BitLocker status")
        else:
            self.add_finding("MEDIUM", "Encryption", "Could not determine BitLocker status",
                             "Run as Administrator for full results")
            print(f"  {YELLOW}WARN{RESET}: BitLocker status unavailable (try running as Admin)")

    # ------------------------------------------------------------------ #
    #  6. Open Network Ports
    # ------------------------------------------------------------------ #
    def check_open_ports(self):
        self.print_section("Open Listening Ports")

        risky_ports = {
            21: "FTP (unencrypted file transfer)",
            23: "Telnet (unencrypted remote access)",
            135: "RPC (common attack target)",
            139: "NetBIOS (SMB file sharing)",
            445: "SMB (common ransomware vector)",
            3389: "RDP (Remote Desktop)",
            5900: "VNC (remote desktop)",
            1433: "MSSQL",
            3306: "MySQL",
            5432: "PostgreSQL",
        }

        out, _, _ = run_cmd("netstat -ano -p TCP")
        listening = []
        if out:
            for line in out.splitlines():
                if "LISTENING" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        addr = parts[1]
                        try:
                            port = int(addr.split(":")[-1])
                            listening.append(port)
                        except ValueError:
                            pass

        found_risky = []
        for port in sorted(set(listening)):
            if port in risky_ports:
                found_risky.append((port, risky_ports[port]))

        if found_risky:
            for port, desc in found_risky:
                sev = "HIGH" if port in (23, 21, 445, 3389) else "MEDIUM"
                self.add_finding(sev, "Network", f"Port {port} is open", desc)
                color = RED if sev == "HIGH" else YELLOW
                print(f"  {color}WARN{RESET}: Port {port} open - {desc}")
        else:
            self.add_finding("PASS", "Network", "No commonly risky ports detected", "")
            print(f"  {GREEN}PASS{RESET}: No commonly risky ports found")

        print(f"  Total listening ports: {len(set(listening))}")

    # ------------------------------------------------------------------ #
    #  7. Password Policy
    # ------------------------------------------------------------------ #
    def check_password_policy(self):
        self.print_section("Password Policy")

        out, _, _ = run_cmd("net accounts")
        if out:
            lines = {line.split(":")[0].strip(): line.split(":")[-1].strip()
                     for line in out.splitlines() if ":" in line}

            min_len_str = lines.get("Minimum password length", "0")
            try:
                min_len = int(min_len_str)
                if min_len < 8:
                    self.add_finding("HIGH", "Passwords", "Minimum password length is too short",
                                     f"Minimum length is {min_len} (recommended: 12+)")
                    print(f"  {RED}FAIL{RESET}: Min password length = {min_len} (recommend 12+)")
                elif min_len < 12:
                    self.add_finding("MEDIUM", "Passwords", "Minimum password length is below recommended",
                                     f"Minimum length is {min_len} (recommended: 12+)")
                    print(f"  {YELLOW}WARN{RESET}: Min password length = {min_len} (recommend 12+)")
                else:
                    self.add_finding("PASS", "Passwords", "Password length policy is adequate", "")
                    print(f"  {GREEN}PASS{RESET}: Min password length = {min_len}")
            except ValueError:
                print(f"  {YELLOW}INFO{RESET}: Could not parse min password length")

            # Lockout threshold
            lockout_str = lines.get("Lockout threshold", "Never")
            if lockout_str.lower() == "never" or lockout_str == "0":
                self.add_finding("MEDIUM", "Passwords", "Account lockout is not configured",
                                 "No lockout threshold allows brute-force attacks")
                print(f"  {YELLOW}WARN{RESET}: Account lockout threshold = Never (brute-force risk)")
            else:
                self.add_finding("PASS", "Passwords", "Account lockout is configured", "")
                print(f"  {GREEN}PASS{RESET}: Account lockout threshold = {lockout_str} attempts")
        else:
            print(f"  {YELLOW}INFO{RESET}: Could not retrieve password policy")

    # ------------------------------------------------------------------ #
    #  8. Guest Account
    # ------------------------------------------------------------------ #
    def check_guest_account(self):
        self.print_section("Guest & Built-in Accounts")

        out, _, _ = run_cmd('net user guest')
        if out and "Account active" in out:
            active = "Yes" in out[out.find("Account active"):]
            if active:
                self.add_finding("HIGH", "Accounts", "Guest account is enabled",
                                 "The Guest account should be disabled")
                print(f"  {RED}FAIL{RESET}: Guest account is ACTIVE")
            else:
                self.add_finding("PASS", "Accounts", "Guest account is disabled", "")
                print(f"  {GREEN}PASS{RESET}: Guest account is disabled")

    # ------------------------------------------------------------------ #
    #  9. Startup Programs (suspicious paths)
    # ------------------------------------------------------------------ #
    def check_startup_programs(self):
        self.print_section("Startup Programs (Suspicious Paths)")

        suspicious_paths = [r"\temp\\", r"\tmp\\", r"\appdata\local\temp\\", r"\downloads\\"]

        out, _, _ = run_cmd(
            'powershell -Command "Get-CimInstance Win32_StartupCommand | Select-Object Name, Command | ConvertTo-Json"'
        )
        found_suspicious = []
        if out:
            try:
                items = json.loads(out) if out.startswith("[") else [json.loads(out)]
                for item in items:
                    cmd = (item.get("Command") or "").lower()
                    name = item.get("Name") or ""
                    for sus in suspicious_paths:
                        if sus in cmd:
                            found_suspicious.append((name, cmd))

                if found_suspicious:
                    for name, cmd in found_suspicious:
                        self.add_finding("HIGH", "Startup", f"Suspicious startup: {name}",
                                         f"Runs from: {cmd[:80]}")
                        print(f"  {RED}WARN{RESET}: Suspicious startup '{name}' -> {cmd[:60]}")
                else:
                    self.add_finding("PASS", "Startup", "No suspicious startup paths detected", "")
                    print(f"  {GREEN}PASS{RESET}: No suspicious startup paths detected")
                    print(f"  Total startup items: {len(items)}")
            except Exception:
                print(f"  {YELLOW}INFO{RESET}: Could not parse startup programs")

    # ------------------------------------------------------------------ #
    # 10. Autorun / AutoPlay
    # ------------------------------------------------------------------ #
    def check_autorun(self):
        self.print_section("AutoRun / AutoPlay")

        out, _, _ = run_cmd(
            r'reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoDriveTypeAutoRun 2>nul'
        )
        # 0xFF (255) disables autorun for all drives
        if "0xff" in out.lower() or "0x91" in out.lower():
            self.add_finding("PASS", "AutoRun", "AutoRun is disabled for all drive types", "")
            print(f"  {GREEN}PASS{RESET}: AutoRun is disabled")
        else:
            self.add_finding("MEDIUM", "AutoRun", "AutoRun may be enabled",
                             "AutoRun can allow malware to execute from USB drives automatically")
            print(f"  {YELLOW}WARN{RESET}: AutoRun may be enabled for some drive types")

    # ------------------------------------------------------------------ #
    # 11. SMBv1
    # ------------------------------------------------------------------ #
    def check_smbv1(self):
        self.print_section("SMBv1 Protocol (EternalBlue)")

        out, _, _ = run_cmd(
            'powershell -Command "(Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol).State"'
        )
        state = out.strip().lower()
        if "disabled" in state:
            self.add_finding("PASS", "Network", "SMBv1 is disabled", "")
            print(f"  {GREEN}PASS{RESET}: SMBv1 is disabled")
        elif "enabled" in state:
            self.add_finding("CRITICAL", "Network", "SMBv1 is ENABLED",
                             "SMBv1 is exploited by EternalBlue/WannaCry ransomware. Disable immediately.")
            print(f"  {RED}CRITICAL{RESET}: SMBv1 is ENABLED - WannaCry/EternalBlue vulnerability!")
        else:
            print(f"  {YELLOW}INFO{RESET}: Could not determine SMBv1 status (may need Admin)")

    # ------------------------------------------------------------------ #
    # 12. Secure Boot
    # ------------------------------------------------------------------ #
    def check_secure_boot(self):
        self.print_section("Secure Boot")

        out, _, _ = run_cmd(
            'powershell -Command "Confirm-SecureBootUEFI"'
        )
        val = out.strip().lower()
        if val == "true":
            self.add_finding("PASS", "Boot", "Secure Boot is enabled", "")
            print(f"  {GREEN}PASS{RESET}: Secure Boot is enabled")
        elif val == "false":
            self.add_finding("HIGH", "Boot", "Secure Boot is disabled",
                             "Secure Boot protects against bootkits and rootkits at startup")
            print(f"  {RED}FAIL{RESET}: Secure Boot is DISABLED")
        else:
            print(f"  {YELLOW}INFO{RESET}: Could not determine Secure Boot status")

    # ------------------------------------------------------------------ #
    # Report
    # ------------------------------------------------------------------ #
    def print_report(self):
        print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
        print(f"{BOLD}  SCAN SUMMARY{RESET}")
        print(f"{BOLD}{CYAN}{'='*60}{RESET}")

        criticals = [f for f in self.findings if f["severity"] == "CRITICAL"]
        highs = [f for f in self.findings if f["severity"] == "HIGH"]

        if criticals:
            print(f"\n{RED}{BOLD}CRITICAL ({len(criticals)}):{RESET}")
            for f in criticals:
                print(f"  [{f['category']}] {f['title']}")
                if f['detail']:
                    print(f"         -> {f['detail']}")

        if highs:
            print(f"\n{RED}HIGH ({len(highs)}):{RESET}")
            for f in highs:
                print(f"  [{f['category']}] {f['title']}")
                if f['detail']:
                    print(f"         -> {f['detail']}")

        if self.warnings:
            mediums = [w for w in self.warnings if w["severity"] == "MEDIUM"]
            lows = [w for w in self.warnings if w["severity"] == "LOW"]
            if mediums:
                print(f"\n{YELLOW}MEDIUM ({len(mediums)}):{RESET}")
                for w in mediums:
                    print(f"  [{w['category']}] {w['title']}")
                    if w['detail']:
                        print(f"         -> {w['detail']}")

        print(f"\n{GREEN}PASSED: {len(self.passed)}{RESET}  |  "
              f"{YELLOW}WARNINGS: {len(self.warnings)}{RESET}  |  "
              f"{RED}ISSUES: {len(self.findings)}{RESET}")

        score = max(0, 100 - len(criticals) * 25 - len(highs) * 10 - len(self.warnings) * 3)
        color = GREEN if score >= 80 else YELLOW if score >= 50 else RED
        print(f"\n{BOLD}Security Score: {color}{score}/100{RESET}")

        # Save JSON report
        report = {
            "scan_time": datetime.now().isoformat(),
            "score": score,
            "critical": criticals,
            "high": highs,
            "warnings": self.warnings,
            "passed": self.passed,
        }
        report_path = Path(__file__).parent / "security_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Full report saved to: {report_path}")

    def run(self):
        self.print_header()
        print("Scanning... (some checks require Administrator privileges)\n")

        self.check_windows_update()
        self.check_antivirus()
        self.check_firewall()
        self.check_uac()
        self.check_bitlocker()
        self.check_open_ports()
        self.check_password_policy()
        self.check_guest_account()
        self.check_startup_programs()
        self.check_autorun()
        self.check_smbv1()
        self.check_secure_boot()

        self.print_report()


if __name__ == "__main__":
    # Encourage running as Admin for full results
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if not is_admin:
        print(f"{YELLOW}NOTE: Some checks work best when run as Administrator.{RESET}")
        print(f"      Right-click your terminal and choose 'Run as administrator'\n")

    scanner = SecurityScanner()
    scanner.run()
