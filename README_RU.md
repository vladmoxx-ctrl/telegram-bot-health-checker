# Telegram Bot Health Checker

Небольшой open-source инструмент для диагностики Telegram-ботов.

Он проверяет валидность токена Telegram Bot API, смотрит статус webhook, при необходимости отправляет тестовое сообщение админу и сохраняет понятный отчёт в JSON и TXT.

Проект специально ограничен **диагностикой ботов**. Он не использует пользовательские Telegram-сессии, не автоматизирует аккаунты, не делает массовые рассылки и не собирает чаты.

## Возможности

- Проверка токена через `getMe`
- Проверка webhook через `getWebhookInfo`
- Предупреждения о типичных конфликтах webhook / polling
- Тестовое сообщение админу
- Отчёты `report.json` и `report.txt`
- Маскирование токена в логах и отчётах
- Работает на Windows, macOS и Linux
- Без обязательных сторонних зависимостей

## Быстрый запуск

```bash
git clone https://github.com/YOUR_USERNAME/telegram-bot-health-checker.git
cd telegram-bot-health-checker
cp .env.example .env
pip install .
python -m telegram_bot_health_checker --env .env
```

Без установки: `PYTHONPATH=src python -m telegram_bot_health_checker --env .env`.

В `.env` укажите `TELEGRAM_BOT_TOKEN` и (необязательно) `TELEGRAM_ADMIN_CHAT_ID`. Понимаются и другие частые имена: `BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `ADMIN_CHAT_ID` — можно проверить бота по его собственному `.env`:

```bash
python -m telegram_bot_health_checker --env /путь/к/боту/.env --no-admin-message
```

## Перед запуском бота с long polling

Бот, который принимает команды через `getUpdates`, не работает, пока у него установлен webhook, и один бот нельзя опрашивать двумя программами. Проверка `webhook` предупреждает о webhook и его последних ошибках; `--delete-webhook` удаляет webhook.

На Windows можно запустить:

```bat
scripts\run_windows.bat
```

## Это не инструмент для спама

В репозитории нет tdata, `.session`, userbot-логики, массовых сообщений, инвайтов, парсинга чатов или обхода ограничений. Это безопасная утилита для разработчиков Telegram-ботов.

## Лицензия

MIT License. См. [LICENSE](LICENSE).
