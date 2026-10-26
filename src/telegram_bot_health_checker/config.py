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


# Accepted variable names, preferred first. The extra names let the checker read
# .env files of bots that use them (for example TELEGRAM_CHAT_ID) and files made
# from the 0.1.0 .env.example, which used BOT_TOKEN and ADMIN_CHAT_ID.
TOKEN_KEYS = ("TELEGRAM_BOT_TOKEN", "BOT_TOKEN")
ADMIN_CHAT_ID_KEYS = ("TELEGRAM_ADMIN_CHAT_ID", "TELEGRAM_CHAT_ID", "ADMIN_CHAT_ID")


def lookup(env_values: dict[str, str], keys: tuple[str, ...]) -> str:
    """First non-empty value: the .env file wins over the process environment."""
    for source in (env_values, os.environ):
        for key in keys:
            value = (source.get(key) or "").strip()
            if value:
                return value
    return ""


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

    resolved_token = (token or lookup(env_values, TOKEN_KEYS)).strip()

    resolved_admin_chat_id = (admin_chat_id or lookup(env_values, ADMIN_CHAT_ID_KEYS)).strip() or None

    return CheckerConfig(
        token=resolved_token,
        admin_chat_id=resolved_admin_chat_id,
        output_dir=Path(output_dir),
        timeout=timeout,
        delete_webhook=delete_webhook,
        send_admin_message=send_admin_message,
    )
