from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class CheckerConfig:
    token: str
    admin_chat_id: str | None = None
    output_dir: Path = Path("reports")
    timeout: float = 15.0
    delete_webhook: bool = False
    send_admin_message: bool = True


def load_dotenv(path: str | Path | None) -> dict[str, str]:
    """Load a simple KEY=VALUE .env file without external dependencies."""
    if path is None:
        return {}

    env_path = Path(path)
    if not env_path.exists():
        raise FileNotFoundError(f".env file not found: {env_path}")

    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def build_config(
    *,
    env_path: str | Path | None,
    token: str | None,
    admin_chat_id: str | None,
    output_dir: str | Path,
    timeout: float,
    delete_webhook: bool,
    send_admin_message: bool,
) -> CheckerConfig:
    env_values = load_dotenv(env_path)

    resolved_token = (
        token
        or env_values.get("TELEGRAM_BOT_TOKEN")
        or os.getenv("TELEGRAM_BOT_TOKEN")
        or ""
    ).strip()

    resolved_admin_chat_id = (
        admin_chat_id
        or env_values.get("TELEGRAM_ADMIN_CHAT_ID")
        or os.getenv("TELEGRAM_ADMIN_CHAT_ID")
        or ""
    ).strip() or None

    return CheckerConfig(
        token=resolved_token,
        admin_chat_id=resolved_admin_chat_id,
        output_dir=Path(output_dir),
        timeout=timeout,
        delete_webhook=delete_webhook,
        send_admin_message=send_admin_message,
    )
