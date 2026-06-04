# Contributing

Thank you for considering a contribution.

This project is focused on safe Telegram Bot API diagnostics for developers and maintainers.

## Good contributions

- Bug fixes
- Better error messages
- Safer token handling
- Better reports
- Documentation improvements
- Tests
- Deployment examples

## Out of scope

The following features will not be accepted:

- User account automation
- Telegram `.session` or `tdata` handling
- Mass messaging
- Scraping chats or users
- Invite automation
- Restriction bypass logic
- Spam or abuse workflows

## Development

```bash
python -m compileall src tests
python -m unittest discover -s tests
python -m telegram_bot_health_checker --help
```
