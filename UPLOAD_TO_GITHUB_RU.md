# Как залить этот проект на GitHub

## Вариант через сайт GitHub

1. Создай новый репозиторий на GitHub.
2. Название: `telegram-bot-health-checker`.
3. Visibility: `Public`.
4. README / License можно не добавлять, они уже есть в архиве.
5. Открой созданный репозиторий.
6. Нажми `Add file` → `Upload files`.
7. Перетащи содержимое этой папки в GitHub.
8. Нажми `Commit changes`.

## Вариант через Git на компьютере

```bash
git init
git add .
git commit -m "Initial open-source release"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot-health-checker.git
git push -u origin main
```

## После загрузки

1. Проверь, что репозиторий публичный.
2. Открой README и убедись, что он красиво отображается.
3. Перейди в `Actions` и убедись, что тесты прошли.
4. Создай первый релиз:
   - Tag: `v0.1.0`
   - Title: `v0.1.0 - Initial open-source release`
   - Description: `Initial safe Telegram Bot API diagnostics release.`
5. После этого можно заполнять форму OpenAI Codex for OSS.

Черновик текста для формы лежит здесь:

```text
docs/openai_codex_for_oss_application_draft.md
```
