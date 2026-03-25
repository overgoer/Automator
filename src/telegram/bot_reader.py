"""
Telegram бот для чтения канала где он админ.
Использует aiogram для long polling.
"""

import logging
from typing import List, Tuple
from datetime import datetime
from aiogram import Bot
from aiogram.types import Message

logger = logging.getLogger(__name__)


class ChannelReaderBot:
    """Чтение постов из канала через бота."""
    
    def __init__(self, bot_token: str, channel: str):
        self.bot_token = bot_token
        self.channel = channel
        self._bot = None
    
    async def connect(self):
        """Инициализация бота."""
        self._bot = Bot(token=self.bot_token)
        
        # Проверка доступа к каналу
        try:
            chat = await self._bot.get_chat(self.channel)
            logger.info(f"Подключено к каналу: {chat.title} ({chat.id})")
        except Exception as e:
            logger.error(f"Нет доступа к каналу: {e}")
            raise RuntimeError(f"Бот не имеет доступа к каналу {self.channel}")
    
    async def close(self):
        """Закрытие бота."""
        if self._bot:
            await self._bot.session.close()
    
    async def get_recent_posts(self, limit: int = 10) -> List[Tuple[int, str, datetime]]:
        """
        Получить последние посты из канала.
        
        Args:
            limit: Количество постов
        
        Returns:
            Список кортежей (message_id, text, date)
        """
        posts = []
        
        # Получаем последние сообщения
        async for message in self._bot.get_updates(
            offset=-limit,
            limit=limit,
            allowed_updates=["channel_post"]
        ):
            if message.channel_post and message.channel_post.text:
                posts.append((
                    message.channel_post.message_id,
                    message.channel_post.text,
                    message.channel_post.date
                ))
        
        # Сортируем по дате (старые сначала)
        posts.sort(key=lambda x: x[2])
        
        logger.info(f"Получено {len(posts)} постов из канала")
        return posts
    
    async def get_last_message_id(self) -> int:
        """Получить ID последнего сообщения в канале."""
        async for message in self._bot.get_updates(
            offset=-1,
            limit=1,
            allowed_updates=["channel_post"]
        ):
            if message.channel_post:
                return message.channel_post.message_id
        
        return 0
