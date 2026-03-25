"""
Automator - минимальная рабочая версия.
Бот слушает канал в реальном времени (long polling).
"""

import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import httpx

load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@eddytester")
USER_ID = int(os.getenv("TELEGRAM_USER_ID", "0"))
AI_API_KEY = os.getenv("AI_API_KEY")

# Глобальные переменные
processed_ids = set()  # ID обработанных постов


async def generate_post(text: str) -> str:
    """Генерация нового поста через DeepSeek."""
    url = "https://api.deepseek.com/chat/completions"
    
    prompt = f"""
Проанализируй этот пост из QA канала:

{text}

Создай новый пост в том же стиле:
- Технический контент без воды
- Эмодзи уместно: 🤘 🔘 ✅ ❌ 🚀 💡
- Короткие абзацы
- Обращение на "ты"

Длина: 500-1000 символов.
Верни только текст поста.
"""
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Ты контент-мейкер для QA канала."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def send_to_user(bot, text: str):
    """Отправка поста пользователю."""
    message = f"🤘 <b>Новый пост готов!</b>\n\n{text}\n\n✅ Готово к публикации"
    
    try:
        await bot.send_message(USER_ID, message, parse_mode="HTML")
        logger.info(f"Отправлено пользователю {USER_ID}")
    except Exception as e:
        logger.error(f"Ошибка отправки: {e}")


async def main():
    """Основной цикл."""
    from aiogram import Bot, Dispatcher
    from aiogram.types import Message
    
    logger.info("=" * 40)
    logger.info("Automator v0.2.0 — бот-админ")
    logger.info(f"Канал: {CHANNEL}")
    logger.info(f"User ID: {USER_ID}")
    logger.info("=" * 40)
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Проверка подключения
    try:
        me = await bot.get_me()
        logger.info(f"Бот: @{me.username}")
        
        chat = await bot.get_chat(CHANNEL)
        logger.info(f"Канал: {chat.title}")
        
        member = await bot.get_chat_member(CHANNEL, me.id)
        if member.status not in ['administrator', 'creator']:
            raise RuntimeError("Бот не админ!")
        logger.info("Бот является админом ✅")
        
    except Exception as e:
        logger.error(f"Ошибка подключения: {e}")
        return
    
    # Хендлер на посты канала
    @dp.channel_post()
    async def handle_post(message: Message):
        if not message.text:
            return
        
        if message.message_id in processed_ids:
            return
        
        logger.info(f"📝 Новый пост #{message.message_id}")
        processed_ids.add(message.message_id)
        
        # Генерация контента
        try:
            logger.info("🤖 Генерация через ИИ...")
            new_post = await generate_post(message.text)
            logger.info(f"✅ Сгенерировано: {len(new_post)} символов")
            
            # Отправка пользователю
            await send_to_user(bot, new_post)
            
        except Exception as e:
            logger.error(f"Ошибка генерации: {e}")
            await send_to_user(bot, f"❌ Ошибка: {e}")
    
    # Запуск
    logger.info("🚀 Запуск polling...")
    logger.info("Слушаю посты в канале...")
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Остановка...")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
