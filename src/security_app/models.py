"""Data models for the Security App."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Severity(str, Enum):
    """Finding severity levels."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    PASS = "PASS"


@dataclass
class Finding:
    """A single security finding produced by a scan."""

    severity: Severity
    category: str
    title: str
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity.value,
            "category": self.category,
            "title": self.title,
            "detail": self.detail,
        }


@dataclass
class ScanReport:
    """Complete security scan report."""

    scan_time: datetime = field(default_factory=datetime.now)
    score: int = 0
    critical: list[Finding] = field(default_factory=list)
    high: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)
    passed: list[Finding] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scan_time": self.scan_time.isoformat(),
            "score": self.score,
            "critical": [f.to_dict() for f in self.critical],
            "high": [f.to_dict() for f in self.high],
            "warnings": [f.to_dict() for f in self.warnings],
            "passed": [f.to_dict() for f in self.passed],
        }


@dataclass
class RemediationRecord:
    """Log entry for a single remediation action."""

    time: datetime
    status: str  # "applied" | "skipped" | "failed"
    action: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "time": self.time.isoformat(),
            "status": self.status,
            "action": self.action,
        }


@dataclass
class OperationalResponse:
    """Standardised response wrapper for audit actions."""

    action: str
    files_touched: list[str]
    commit_hash: str | None = None
    risk_level: str = "Low"
    next_recommendation: str = "Monitor performance."

    def to_dict(self) -> dict[str, Any]:
        return {
            "🔍 Action Taken": self.action,
            "📦 Files Touched": self.files_touched,
            "📦 Git Commit Hash": self.commit_hash or "N/A",
            "⚠️ Risk Level": self.risk_level,
            "🛠 Next Recommendation": self.next_recommendation,
        }
