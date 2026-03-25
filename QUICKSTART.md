# Automator — Быстрый старт

## 🚀 Запуск за 1 минуту

### 1. Проверь что бот — админ в канале

@mrgriffbot должен быть админом в @eddytester ✅ (уже сделано)

### 2. Запусти бота

```bash
cd /Users/eddy/IdeaProjects/Automator
python3 run.py
```

### 3. Готово!

Бот слушает канал. Когда появится новый пост:
1. 📖 Бот прочитает пост
2. 🤖 Отправит в DeepSeek для генерации
3. 📩 Присылает готовый пост тебе в Telegram (@edtext)

---

## Как это работает

```
@eddytester (новый пост) 
    ↓
@mrgriffbot (читает как админ)
    ↓
DeepSeek AI (генерирует контент)
    ↓
@edtext (ты получаешь готовый пост)
```

**Важно**: Бот работает в реальном времени. Он обрабатывает посты **по мере их появления**.

---

## Постоянная работа

### Вариант A: Локально (тест)
```bash
python3 run.py
```
Работает пока терминал открыт.

### Вариант B: Сервер (прода)
```bash
# В фоне
nohup python3 run.py > automator.log 2>&1 &

# Или как systemd сервис
sudo systemctl enable automator
sudo systemctl start automator
```

### Вариант C: Docker
```bash
docker-compose up -d
```

---

## Конфигурация (.env)

```env
TELEGRAM_BOT_TOKEN=8731416921:AAHMeNtEAXtPZaRTcivOTqfzTU1tbFXI6m4
TELEGRAM_CHANNEL=@eddytester
TELEGRAM_USER_ID=79068819
AI_API_KEY=sk-7419b988a84a4c768489bcc5a35f6175
```

---

## Тестирование

1. Запусти бота: `python3 run.py`
2. Опубликуй тестовый пост в @eddytester
3. Через 5-10 секунд получишь готовый пост в личку

---

## Проблемы?

| Ошибка | Решение |
|--------|---------|
| "Бот не админ" | Добавь @mrgriffbot админом в канал |
| "Invalid token" | Проверь токен в @BotFather |
| "API key invalid" | Проверь ключ DeepSeek |
| Бот не отвечает | Проверь логи: `tail -f automator.log` |

---

**v0.2.0** — бот-админ, реальное время
