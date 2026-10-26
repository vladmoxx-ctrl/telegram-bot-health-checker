# Telegram Bot Health Checker

A small open-source diagnostics tool for Telegram bot developers.

It checks whether a Telegram Bot API token is valid, reads webhook status, optionally sends a test message to an admin chat, and writes a clear health report in JSON and text formats.

This project is intentionally limited to **bot diagnostics**. It does not use Telegram user sessions, does not automate user accounts, does not send bulk messages, and does not scrape chats.

## Features

- Validate a Telegram bot token with `getMe`
- Read webhook status with `getWebhookInfo`
- Detect common webhook / polling configuration warnings
- Optionally send a test notification to an admin chat
- Generate `report.json` and `report.txt`
- Mask sensitive tokens in logs and reports
- Works on Windows, macOS, and Linux
- No third-party runtime dependencies

## What this project is not

This repository is not a spam tool, userbot tool, account checker, mass sender, invite tool, scraper, or restriction bypass tool. It is a safe diagnostics utility for developers who maintain Telegram bots.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/telegram-bot-health-checker.git
cd telegram-bot-health-checker
```

### 2. Create a configuration file

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 3. Install and run the checker

```bash
pip install .
python -m telegram_bot_health_checker --env .env
```

Without installing, point Python at the `src` folder:

```bash
PYTHONPATH=src python -m telegram_bot_health_checker --env .env
```

On Windows, `scripts\run_windows.bat` does this for you.

Or without a `.env` file:

```bash
python -m telegram_bot_health_checker --token "123456:ABC..." --admin-chat-id "123456789"
```

### 4. View the report

By default, reports are written to:

```text
reports/report.json
reports/report.txt
```

## Example output

```text
Telegram Bot Health Checker
Status: OK

Checks:
- token: OK — Bot token is valid. Bot: @example_bot
- webhook: OK — No webhook is configured. Polling can be used.
- admin_message: OK — Test message sent to admin chat.
```

## CLI options

```text
--env PATH              Path to .env file
--token TOKEN           Telegram Bot API token
--admin-chat-id ID      Optional admin chat ID for a test message
--output-dir PATH       Directory for report.json and report.txt
--timeout SECONDS       HTTP timeout, default: 15
--delete-webhook        Delete the current webhook before checking status
--no-admin-message      Do not send a test admin notification
--json                  Print JSON report to stdout
```

## Configuration

`.env.example`:

```env
TELEGRAM_BOT_TOKEN=replace_me_with_botfather_token
TELEGRAM_ADMIN_CHAT_ID=123456789
```

`TELEGRAM_ADMIN_CHAT_ID` is optional. If it is not set, the checker will skip the admin notification test.

The checker also understands `.env` files of bots that use other common names: `BOT_TOKEN` for the token and `TELEGRAM_CHAT_ID` or `ADMIN_CHAT_ID` for the chat. So you can point it at your bot's own `.env` (add `--no-admin-message` if you do not want a test message):

```bash
python -m telegram_bot_health_checker --env /path/to/your-bot/.env --no-admin-message
```

## Before running a bot with long polling

A bot that reads commands with `getUpdates` (long polling) cannot work while a webhook is set, and two programs must not poll the same bot. The `webhook` check warns about a configured webhook or a recent webhook error. `--delete-webhook` removes the webhook so polling can start.

## Exit codes

- `0` — all critical checks passed
- `1` — one or more warnings were found
- `2` — one or more critical errors were found

## Use cases

- Confirm that a bot token is valid before deployment
- Verify webhook status after switching between webhook and polling mode
- Check that the admin notification channel works
- Generate a simple diagnostics report for maintainers or support teams
- Add a safe preflight check to bot deployment scripts

## Security

Never commit `.env`, tokens, chat IDs, session files, or private logs. See [SECURITY.md](SECURITY.md) for responsible disclosure and safe usage notes.

## Roadmap

- GitHub Actions example for scheduled checks (tests already run in CI)
- Docker image
- HTML report
- Optional Prometheus-compatible output
- More deployment examples for VPS/server environments

## Contributing

Pull requests are welcome. Please keep the project focused on safe bot diagnostics and developer tooling. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License. See [LICENSE](LICENSE).
