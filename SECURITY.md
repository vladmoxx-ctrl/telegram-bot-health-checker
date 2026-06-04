# Security Policy

## Supported versions

Security fixes are provided for the latest release.

## Safe usage rules

- Never commit real bot tokens.
- Never commit `.env` files.
- Never commit Telegram user session files such as `.session` or `tdata`.
- Never commit private logs, chat IDs, account exports, or customer data.
- Use `.env.example` for documentation and local `.env` for secrets.

## Responsible disclosure

If you find a security issue, please open a private security advisory on GitHub or contact the maintainer privately. Do not publish exploit details before a fix is available.
