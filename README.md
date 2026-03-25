# Automator

ИИ-контент креатор для Telegram канала @eddytester.

Автоматически анализирует посты канала → генерирует новый контент через DeepSeek → отправляет готовый пост.

**Статус**: v0.1.0 (MVP)

📋 [Бэклог и дорожная карта](BACKLOG.md) | 🏗 [Архитектура](architecture.md)

---

## Возможности

- ✅ Чтение постов из Telegram канала (без картинок, только текст)
- ✅ Генерация контента через DeepSeek AI в стиле канала
- ✅ Отправка готового поста в Telegram (в личку)
- ✅ Работа по расписанию (каждые 2 дня)
- ✅ Автоматический запуск через GitHub Actions
- ✅ Сохранение истории в SQLite

---

## Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/overgoer/Automator.git
cd Automator
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Заполните `.env`:

```env
# Telegram API (получить на my.telegram.org)
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890

# Канал
TELEGRAM_CHANNEL=@eddytester

# DeepSeek AI
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

# Telegram бот для уведомлений
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_USER_ID=123456789
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Создание Telegram сессии

```bash
python scripts/create_session.py
```

Введите номер телефона второго аккаунта и код из Telegram.

### 5. Тестовый запуск

```bash
python -m src.main
```

---

## Настройка GitHub Actions

### 1. Добавление секретов

В репозитории на GitHub:
**Settings → Secrets and variables → Actions → New repository secret**

Добавьте секреты:

| Название | Значение |
|----------|----------|
| `TELEGRAM_API_ID` | Ваш API ID |
| `TELEGRAM_API_HASH` | Ваш API HASH |
| `TELEGRAM_CHANNEL` | `@eddytester` |
| `AI_API_KEY` | Ключ DeepSeek |
| `TELEGRAM_BOT_TOKEN` | Токен бота |
| `TELEGRAM_USER_ID` | Ваш User ID |

### 2. Запуск workflow

Workflow запускается:
- Автоматически: каждые 2 дня в 00:00 UTC
- Вручную: **Actions → Automator → Run workflow**

---

## Структура проекта

```
Automator/
├── .env                      # Переменные окружения (не в git)
├── .env.example              # Шаблон переменных
├── requirements.txt          # Зависимости Python
├── architecture.md           # Архитектура проекта
├── requirements.md           # Требования
│
├── .github/workflows/
│   └── automator.yml         # GitHub Actions workflow
│
├── src/
│   ├── main.py               # Точка входа
│   ├── config.py             # Конфигурация
│   │
│   ├── db/
│   │   ├── models.py         # Модели данных
│   │   └── repository.py     # CRUD операции
│   │
│   ├── telegram/
│   │   ├── client.py         # Telegram клиент
│   │   └── scraper.py        # Скрапер постов
│   │
│   ├── ai/
│   │   ├── client.py         # DeepSeek клиент
│   │   └── prompt.py         # Промпты для ИИ
│   │
│   └── notifier/
│       └── telegram_bot.py   # Уведомления
│
├── scripts/
│   └── create_session.py     # Создание сессии Telegram
│
├── logs/
│   └── automator.log         # Логи
│
└── tests/
    └── ...                   # Тесты
```

---

## Стиль контента

На основе анализа канала @eddytester:

- **Тон**: технический, без воды, с юмором
- **Эмодзи**: 🤘 🔘 ✅ ❌ 🚀 💡 🧠 📌
- **Хэштеги**: #memes #оффтоп #ДорогойБаг
- **Формат**: заголовок → текст → выводы/ссылки
- **Обращение**: на "ты"

---

## Логи

Логи сохраняются в `logs/automator.log`.

Для просмотра в реальном времени:

```bash
tail -f logs/automator.log
```

---

## Расширение функционала

### Добавление новых типов контента

В `src/ai/prompt.py` добавьте новый промпт:

```python
WEEKLY_DIGEST_PROMPT = """
...
"""
```

### Изменение расписания

В `.github/workflows/automator.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Каждый день
```

### Добавление email уведомлений

Создайте `src/notifier/email.py` по аналогии с `telegram_bot.py`.

---

## Troubleshooting

### Ошибка "Клиент не авторизован"

Запустите заново:

```bash
python scripts/create_session.py
```

### Ошибка "AI API key invalid"

Проверьте ключ DeepSeek в личном кабинете: https://platform.deepseek.com/

### Workflow не запускается

Проверьте:
1. Секреты добавлены в Settings → Secrets
2. Workflow не заблокирован (Actions → Enable workflow)

---

## Лицензия

MIT
