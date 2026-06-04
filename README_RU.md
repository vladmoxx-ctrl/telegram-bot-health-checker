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
python -m telegram_bot_health_checker --env .env
```

На Windows можно запустить:

```bat
scripts\run_windows.bat
```

## Это не инструмент для спама

В репозитории нет tdata, `.session`, userbot-логики, массовых сообщений, инвайтов, парсинга чатов или обхода ограничений. Это безопасная утилита для разработчиков Telegram-ботов.

## Лицензия

MIT License. См. [LICENSE](LICENSE).
