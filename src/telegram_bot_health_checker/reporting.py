from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    message: str
    details: dict[str, object] | None = None


@dataclass(frozen=True)
class HealthReport:
    status: str
    summary: str
    generated_at: str
    checks: list[CheckResult]


def mask_token(token: str) -> str:
    if not token:
        return ""
    if len(token) <= 12:
        return "***"
    if ":" in token:
        left, right = token.split(":", 1)
        left_masked = left[:3] + "***" + left[-2:] if len(left) > 5 else "***"
        right_masked = right[:4] + "***" + right[-4:] if len(right) > 8 else "***"
        return f"{left_masked}:{right_masked}"
    return token[:4] + "***" + token[-4:]


def redact_sensitive_text(text: str) -> str:
    """Redact Telegram Bot API tokens from arbitrary text."""
    token_pattern = re.compile(r"\b\d{5,}:[A-Za-z0-9_-]{20,}\b")
    return token_pattern.sub("<redacted-token>", text)


def build_report(checks: list[CheckResult]) -> HealthReport:
    has_error = any(c.status == "ERROR" for c in checks)
    has_warning = any(c.status == "WARNING" for c in checks)

    if has_error:
        status = "ERROR"
        summary = "One or more critical checks failed."
    elif has_warning:
        status = "WARNING"
        summary = "Checks passed with warnings."
    else:
        status = "OK"
        summary = "All critical checks passed."

    return HealthReport(
        status=status,
        summary=summary,
        generated_at=datetime.now(timezone.utc).isoformat(),
        checks=checks,
    )


def report_to_json(report: HealthReport) -> str:
    return json.dumps(asdict(report), ensure_ascii=False, indent=2)


def report_to_text(report: HealthReport) -> str:
    lines = [
        "Telegram Bot Health Checker",
        f"Status: {report.status}",
        f"Generated at: {report.generated_at}",
        "",
        report.summary,
        "",
        "Checks:",
    ]
    for check in report.checks:
        lines.append(f"- {check.name}: {check.status} — {check.message}")
    return "\n".join(lines) + "\n"


def write_report(report: HealthReport, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "report.json"
    text_path = output_dir / "report.txt"

    json_path.write_text(report_to_json(report), encoding="utf-8")
    text_path.write_text(report_to_text(report), encoding="utf-8")

    return json_path, text_path
