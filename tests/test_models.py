"""Tests for data models."""

from datetime import datetime

from security_app.models import (
    Finding,
    OperationalResponse,
    RemediationRecord,
    ScanReport,
    Severity,
)


def test_finding_to_dict():
    f = Finding(Severity.HIGH, "Network", "Port open", "Port 445")
    d = f.to_dict()
    assert d["severity"] == "HIGH"
    assert d["category"] == "Network"
    assert d["title"] == "Port open"
    assert d["detail"] == "Port 445"


def test_scan_report_to_dict():
    report = ScanReport(score=75)
    report.high.append(Finding(Severity.HIGH, "Net", "Port 445", "SMB"))
    d = report.to_dict()
    assert d["score"] == 75
    assert len(d["high"]) == 1
    assert "scan_time" in d


def test_remediation_record_to_dict():
    now = datetime(2026, 1, 1, 12, 0, 0)
    rec = RemediationRecord(time=now, status="applied", action="Block SMB 445")
    d = rec.to_dict()
    assert d["status"] == "applied"
    assert d["action"] == "Block SMB 445"
    assert "2026-01-01" in d["time"]


def test_operational_response_to_dict():
    resp = OperationalResponse(
        action="Audit run",
        files_touched=["security_scan.py"],
        commit_hash="abc123",
        risk_level="Low",
        next_recommendation="Monitor.",
    )
    d = resp.to_dict()
    assert d["🔍 Action Taken"] == "Audit run"
    assert d["📦 Git Commit Hash"] == "abc123"


def test_operational_response_no_commit():
    resp = OperationalResponse(action="Test", files_touched=[])
    d = resp.to_dict()
    assert d["📦 Git Commit Hash"] == "N/A"


def test_severity_enum_values():
    assert Severity.CRITICAL == "CRITICAL"
    assert Severity.HIGH == "HIGH"
    assert Severity.PASS == "PASS"
