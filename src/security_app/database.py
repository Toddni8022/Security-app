"""Database operations for the Security App."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ReportStore:
    """Simple JSON-file-backed store for scan reports and remediation logs."""

    def __init__(self, base_dir: str | Path = "./reports") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    # ── scan reports ───────────────────────────────────────────────────────────

    def save_report(self, report: dict[str, Any], filename: str | None = None) -> Path:
        """Persist *report* as JSON and return the file path."""
        if filename is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"{date_str}_report.json"
        path = self.base_dir / filename
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        logger.info("Report saved to %s", path)
        return path

    def load_report(self, filename: str) -> dict[str, Any] | None:
        """Load a report by filename; return *None* if not found."""
        path = self.base_dir / filename
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def latest_report(self) -> dict[str, Any] | None:
        """Return the most recently saved report, or *None*."""
        reports = sorted(self.base_dir.glob("*_report.json"))
        if not reports:
            return None
        return json.loads(reports[-1].read_text(encoding="utf-8"))

    # ── remediation logs ───────────────────────────────────────────────────────

    def save_remediation_log(
        self, log_data: dict[str, Any], path: str | Path | None = None
    ) -> Path:
        """Persist a remediation log and return its path."""
        if path is None:
            path = self.base_dir.parent / "remediation_log.json"
        path = Path(path)
        path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")
        logger.info("Remediation log saved to %s", path)
        return path
