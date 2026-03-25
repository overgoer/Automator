"""
Telegram клиент для чтения канала через бота.
Использует Telethon с бот-токеном (не требует API_ID/HASH).
"""

import logging
from typing import List, Tuple, Optional
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.types import Message

logger = logging.getLogger(__name__)


class BotTelegramClient:
    """Telethon клиент с бот-токеном."""
    
    def __init__(self, bot_token: str, channel: str):
        self.bot_token = bot_token
        self.channel = channel
        self._client: Optional[TelegramClient] = None
    
    async def connect(self):
        """Подключение к Telegram как бот."""
        # Извлекаем бот ID из токена (формат: 123456:ABC-DEF...)
        bot_id = self.bot_token.split(':')[0]
        
        self._client = TelegramClient(
            f"bot_session_{bot_id}",
            api_id=2040,  # Публичный, для подключения
            api_hash="b18441a1ff607e11a989891a5462e627",
            bot=self.bot_token
        )
        
        await self._client.connect()
        
        # Проверка доступа к каналу
        try:
            entity = await self._client.get_entity(self.channel)
            logger.info(f"Бот подключён к каналу: {entity.title}")
        except Exception as e:
            logger.error(f"Нет доступа к каналу: {e}")
            await self.disconnect()
            raise RuntimeError(f"Бот не имеет доступа к каналу {self.channel}")
    
    async def disconnect(self):
        """Отключение от Telegram."""
        if self._client:
            await self._client.disconnect()
            logger.info("Бот отключён от Telegram")
    
    async def get_channel_messages(
        self,
        min_id: int = 0,
        limit: int = 50
    ) -> List[Message]:
        """
        Получить сообщения из канала.
        
        Args:
            min_id: Получать сообщения с ID больше этого
            limit: Максимальное количество сообщений
        
        Returns:
            Список сообщений
        """
        if not self._client:
            raise RuntimeError("Клиент не подключён")
        
        entity = await self._client.get_entity(self.channel)
        
        messages = []
        async for message in self._client.iter_messages(
            entity,
            min_id=min_id if min_id > 0 else None,
            limit=limit
        ):
            if message.text:  # Только сообщения с текстом
                messages.append(message)
        
        logger.info(f"Получено {len(messages)} сообщений из канала")
        return messages
    
    async def get_last_message_id(self) -> Optional[int]:
        """Получить ID последнего сообщения в канале."""
        if not self._client:
            return None
        
        entity = await self._client.get_entity(self.channel)
        async for message in self._client.iter_messages(entity, limit=1):
            return message.id
        
        return None
