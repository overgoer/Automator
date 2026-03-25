"""
Telegram бот для чтения канала через aiogram long polling.
Бот получает посты когда они публикуются (real-time).
"""

import logging
from typing import Optional, Callable, Awaitable
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

logger = logging.getLogger(__name__)


class ChannelListener:
    """Слушает посты в канале через бота-админа."""
    
    def __init__(self, bot_token: str, channel: str):
        self.bot_token = bot_token
        self.channel = channel
        self._bot: Optional[Bot] = None
        self._dp: Optional[Dispatcher] = None
        self._on_post_callback: Optional[Callable] = None
        self._last_message_id: int = 0
    
    async def connect(self):
        """Инициализация бота и проверка доступа."""
        self._bot = Bot(token=self.bot_token)
        self._dp = Dispatcher()
        
        # Проверка доступа к каналу
        try:
            chat = await self._bot.get_chat(self.channel)
            logger.info(f"Бот подключён к каналу: {chat.title} ({chat.id})")
            
            # Проверяем что бот админ
            me = await self._bot.get_me()
            member = await self._bot.get_chat_member(self.channel, me.id)
            if member.status not in ['administrator', 'creator']:
                raise RuntimeError("Бот не админ в канале!")
            
            logger.info("Бот является админом в канале ✅")
                
        except Exception as e:
            logger.error(f"Нет доступа к каналу: {e}")
            raise RuntimeError(f"Бот не имеет доступа к каналу {self.channel}")
        
        # Регистрируем хендлер на посты канала
        @self._dp.channel_post()
        async def handle_channel_post(message: Message):
            if message.text:
                logger.info(f"Новый пост #{message.message_id}: {len(message.text)} символов")
                self._last_message_id = message.message_id
                
                if self._on_post_callback:
                    await self._on_post_callback(
                        message.message_id,
                        message.text,
                        message.date
                    )
    
    async def close(self):
        """Закрытие бота."""
        if self._bot:
            await self._bot.session.close()
    
    def on_post(self, callback: Callable):
        """Установить callback на новые посты."""
        self._on_post_callback = callback
    
    async def start_polling(self):
        """Запуск long polling (бесконечный цикл)."""
        logger.info("Запуск polling...")
        await self._dp.start_polling(self._bot)
    
    async def get_recent_posts(self, limit: int = 10) -> list:
        """
        Получить последние посты.
        NOTE: aiogram не может получить историю, только новые посты.
        Для MVP возвращаем заглушку.
        """
        logger.warning("get_recent_posts не доступен для aiogram бота")
        return []
