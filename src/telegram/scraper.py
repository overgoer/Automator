"""
Скрапер постов из Telegram канала.
"""

import logging
from datetime import datetime
from typing import List, Tuple

from .client import TelegramClientWrapper

logger = logging.getLogger(__name__)


class PostScraper:
    """Скачивание постов из Telegram канала."""
    
    def __init__(self, tg_client: TelegramClientWrapper, channel: str):
        self.tg_client = tg_client
        self.channel = channel
    
    async def fetch_new_posts(
        self,
        last_processed_id: int = 0
    ) -> List[Tuple[int, str, datetime]]:
        """
        Получить новые посты из канала.
        
        Args:
            last_processed_id: ID последнего обработанного сообщения
        
        Returns:
            Список кортежей (message_id, text, date)
        """
        messages = await self.tg_client.get_channel_messages(
            self.channel,
            min_id=last_processed_id,
            limit=50
        )
        
        posts = []
        for msg in messages:
            if msg.text and not msg.media:  # Только текст, без картинок
                posts.append((
                    msg.id,
                    msg.text,
                    msg.date
                ))
                logger.debug(f"Пост {msg.id}: {len(msg.text)} символов")
        
        # Сортируем по дате (старые сначала)
        posts.sort(key=lambda x: x[2])
        
        logger.info(f"Найдено {len(posts)} новых постов")
        return posts
    
    async def fetch_latest_posts(self, limit: int = 10) -> List[Tuple[int, str, datetime]]:
        """
        Получить последние N постов из канала.
        
        Args:
            limit: Количество постов
        
        Returns:
            Список кортежей (message_id, text, date)
        """
        messages = await self.tg_client.get_channel_messages(
            self.channel,
            limit=limit
        )
        
        posts = []
        for msg in messages:
            if msg.text and not msg.media:  # Только текст
                posts.append((
                    msg.id,
                    msg.text,
                    msg.date
                ))
        
        posts.sort(key=lambda x: x[2])
        return posts
