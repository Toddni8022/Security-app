"""Shared utility functions."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any


def operational_response(
    action: str,
    files_touched: list[str],
    commit_hash: str | None = None,
    risk_level: str = "Low",
    next_recommendation: str = "Monitor performance.",
) -> dict[str, Any]:
    """Return a standardised operational response dictionary."""
    return {
        "🔍 Action Taken": action,
        "📦 Files Touched": files_touched,
        "📦 Git Commit Hash": commit_hash if commit_hash else "N/A",
        "⚠️ Risk Level": risk_level,
        "🛠 Next Recommendation": next_recommendation,
    }


def check_daily_report(reports_dir: str = "./reports") -> str:
    """Return today's report summary or an appropriate message."""
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = Path(reports_dir) / f"{today}_report.txt"
    if report_path.exists():
        summary = report_path.read_text(encoding="utf-8").strip()
        return f"Summary for {today}:\n{summary}"
    return "No audit report was run today."


def ensure_dir(path: str | Path) -> Path:
    """Create *path* (and any parents) if it does not already exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def redact_sensitive(value: str, visible: int = 4) -> str:
    """Return *value* with all but the last *visible* characters masked."""
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]
