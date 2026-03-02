"""Tests for scanner modules."""

import pytest

from security_app.models import Finding, Severity
from security_app.scanner.vulnerability import assess_score, run_command


def test_assess_score_no_findings():
    assert assess_score([]) == 100


def test_assess_score_critical():
    findings = [Finding(Severity.CRITICAL, "Test", "Critical issue")]
    assert assess_score(findings) == 75


def test_assess_score_mixed():
    findings = [
        Finding(Severity.HIGH, "Network", "Port open"),
        Finding(Severity.MEDIUM, "AutoRun", "AutoRun enabled"),
    ]
    assert assess_score(findings) == 80  # 100 - 15 - 5


def test_assess_score_floor():
    findings = [Finding(Severity.CRITICAL, "Cat", "Issue")] * 10
    assert assess_score(findings) == 0


def test_run_command_success():
    stdout, stderr, rc = run_command("echo hello")
    assert "hello" in stdout
    assert rc == 0


def test_run_command_timeout():
    stdout, stderr, rc = run_command("sleep 60", timeout=1)
    assert rc == -1
    assert "TIMEOUT" in stderr
