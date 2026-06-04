from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .client import TelegramApiError, TelegramBotApiClient
from .config import build_config
from .reporting import CheckResult, build_report, mask_token, report_to_json, report_to_text, write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="telegram-bot-health-checker",
        description="Safe Telegram Bot API health checker for developers.",
    )
    parser.add_argument("--env", default=None, help="Path to .env file")
    parser.add_argument("--token", default=None, help="Telegram Bot API token")
    parser.add_argument("--admin-chat-id", default=None, help="Optional admin chat ID for a test message")
    parser.add_argument("--output-dir", default="reports", help="Directory for report.json and report.txt")
    parser.add_argument("--timeout", default=15.0, type=float, help="HTTP timeout in seconds")
    parser.add_argument("--delete-webhook", action="store_true", help="Delete current webhook before checking status")
    parser.add_argument("--no-admin-message", action="store_true", help="Do not send a test admin notification")
    parser.add_argument("--json", action="store_true", help="Print JSON report to stdout")
    return parser


def validate_token_format(token: str) -> CheckResult | None:
    if not token:
        return CheckResult(
            name="config",
            status="ERROR",
            message="Telegram bot token is missing. Set TELEGRAM_BOT_TOKEN or pass --token.",
        )
    if ":" not in token or len(token) < 20:
        return CheckResult(
            name="config",
            status="ERROR",
            message="Telegram bot token format looks invalid.",
            details={"token": mask_token(token)},
        )
    return None


def run_checks(config) -> list[CheckResult]:
    checks: list[CheckResult] = []

    config_error = validate_token_format(config.token)
    if config_error is not None:
        return [config_error]

    client = TelegramBotApiClient(token=config.token, timeout=config.timeout)

    try:
        me = client.get_me()
        username = me.get("username")
        bot_id = me.get("id")
        checks.append(
            CheckResult(
                name="token",
                status="OK",
                message=f"Bot token is valid. Bot: @{username}" if username else "Bot token is valid.",
                details={"bot_id": bot_id, "username": username},
            )
        )
    except TelegramApiError as exc:
        return [
            CheckResult(
                name="token",
                status="ERROR",
                message=str(exc),
                details={"token": mask_token(config.token)},
            )
        ]

    if config.delete_webhook:
        try:
            client.delete_webhook()
            checks.append(
                CheckResult(
                    name="delete_webhook",
                    status="OK",
                    message="Webhook delete request completed.",
                )
            )
        except TelegramApiError as exc:
            checks.append(
                CheckResult(
                    name="delete_webhook",
                    status="WARNING",
                    message=f"Could not delete webhook: {exc}",
                )
            )

    try:
        webhook = client.get_webhook_info()
        webhook_url = webhook.get("url") or ""
        pending = webhook.get("pending_update_count", 0)
        last_error_message = webhook.get("last_error_message")

        if last_error_message:
            checks.append(
                CheckResult(
                    name="webhook",
                    status="WARNING",
                    message=f"Webhook has a recent error: {last_error_message}",
                    details={"pending_update_count": pending, "has_webhook": bool(webhook_url)},
                )
            )
        elif webhook_url:
            checks.append(
                CheckResult(
                    name="webhook",
                    status="WARNING",
                    message="Webhook is configured. Polling mode should not run at the same time.",
                    details={"pending_update_count": pending, "has_webhook": True},
                )
            )
        else:
            checks.append(
                CheckResult(
                    name="webhook",
                    status="OK",
                    message="No webhook is configured. Polling can be used.",
                    details={"pending_update_count": pending, "has_webhook": False},
                )
            )
    except TelegramApiError as exc:
        checks.append(
            CheckResult(
                name="webhook",
                status="WARNING",
                message=f"Could not read webhook info: {exc}",
            )
        )

    if config.admin_chat_id and config.send_admin_message:
        try:
            client.send_message(
                config.admin_chat_id,
                "✅ Telegram Bot Health Checker: test notification delivered.",
            )
            checks.append(
                CheckResult(
                    name="admin_message",
                    status="OK",
                    message="Test message sent to admin chat.",
                )
            )
        except TelegramApiError as exc:
            checks.append(
                CheckResult(
                    name="admin_message",
                    status="WARNING",
                    message=f"Could not send admin test message: {exc}",
                )
            )
    elif config.admin_chat_id and not config.send_admin_message:
        checks.append(
            CheckResult(
                name="admin_message",
                status="OK",
                message="Admin chat ID is configured. Test message skipped by --no-admin-message.",
            )
        )
    else:
        checks.append(
            CheckResult(
                name="admin_message",
                status="WARNING",
                message="Admin chat ID is not configured, so the notification test was skipped.",
            )
        )

    return checks


def exit_code_for_status(status: str) -> int:
    if status == "ERROR":
        return 2
    if status == "WARNING":
        return 1
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = build_config(
            env_path=args.env,
            token=args.token,
            admin_chat_id=args.admin_chat_id,
            output_dir=args.output_dir,
            timeout=args.timeout,
            delete_webhook=args.delete_webhook,
            send_admin_message=not args.no_admin_message,
        )
    except Exception as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    checks = run_checks(config)
    report = build_report(checks)
    json_path, text_path = write_report(report, config.output_dir)

    if args.json:
        print(report_to_json(report))
    else:
        print(report_to_text(report))
        print(f"Reports written to: {json_path} and {text_path}")

    return exit_code_for_status(report.status)


if __name__ == "__main__":
    raise SystemExit(main())
