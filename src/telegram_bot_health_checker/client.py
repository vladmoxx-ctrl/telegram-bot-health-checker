from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib import error, parse, request


class TelegramApiError(RuntimeError):
    pass


@dataclass(frozen=True)
class TelegramBotApiClient:
    token: str
    timeout: float = 15.0

    @property
    def base_url(self) -> str:
        return f"https://api.telegram.org/bot{self.token}/"

    def call(self, method: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        url = self.base_url + method
        payload = None
        headers = {"User-Agent": "telegram-bot-health-checker/0.1.0"}

        if data is not None:
            payload = parse.urlencode(data).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        req = request.Request(url, data=payload, headers=headers, method="POST" if data else "GET")

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8", errors="replace")
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise TelegramApiError(f"Telegram API HTTP {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise TelegramApiError(f"Network error: {exc.reason}") from exc
        except TimeoutError as exc:
            raise TelegramApiError("Request timed out") from exc

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise TelegramApiError("Telegram API returned invalid JSON") from exc

        if not isinstance(parsed, dict):
            raise TelegramApiError("Telegram API returned an unexpected response")

        if not parsed.get("ok"):
            description = parsed.get("description", "Unknown Telegram API error")
            raise TelegramApiError(str(description))

        return parsed

    def get_me(self) -> dict[str, Any]:
        return self.call("getMe").get("result", {})

    def get_webhook_info(self) -> dict[str, Any]:
        return self.call("getWebhookInfo").get("result", {})

    def delete_webhook(self) -> dict[str, Any]:
        return self.call("deleteWebhook", {"drop_pending_updates": "false"}).get("result", {})

    def send_message(self, chat_id: str, text: str) -> dict[str, Any]:
        return self.call("sendMessage", {"chat_id": chat_id, "text": text}).get("result", {})
