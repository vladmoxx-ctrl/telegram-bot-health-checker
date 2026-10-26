# Changelog

## v0.1.1

- Fix `.env.example`: it used `BOT_TOKEN` / `ADMIN_CHAT_ID`, which the checker did not read, so a copied example always failed with "token is missing". The example now uses `TELEGRAM_BOT_TOKEN` / `TELEGRAM_ADMIN_CHAT_ID`.
- Also accept `BOT_TOKEN`, `TELEGRAM_CHAT_ID` and `ADMIN_CHAT_ID`, so a bot's own `.env` can be checked as is.
- Add `.gitignore` for `.env`, reports and Python build output.
- Windows launcher and README: run from the `src` layout without installing, or `pip install .`.
- Run the tests in GitHub Actions.

## v0.1.0 - Initial open-source release

- Initial Telegram Bot API token validation
- Webhook diagnostics
- Optional admin test message
- JSON and text reports
- Safe secret masking
- English and Russian documentation
