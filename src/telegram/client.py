"""
Telegram клиент для чтения постов из канала.
Использует Telethon для авторизации и получения сообщений.
"""

import logging
from typing import Optional, List, Tuple
from telethon import TelegramClient
from telethon.tl.types import Message

logger = logging.getLogger(__name__)


class TelegramClientWrapper:
    """Обёртка над Telethon клиентом."""
    
    def __init__(self, api_id: int, api_hash: str, session_name: str = "automator"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self._client: Optional[TelegramClient] = None
    
    async def connect(self):
        """Подключение к Telegram."""
        self._client = TelegramClient(
            self.session_name,
            self.api_id,
            self.api_hash
        )
        await self._client.connect()
        
        if not await self._client.is_user_authorized():
            logger.error("Клиент не авторизован. Запустите get_telegram_session.py")
            raise RuntimeError("Требуется авторизация клиента")
        
        logger.info("Подключено к Telegram")
    
    async def disconnect(self):
        """Отключение от Telegram."""
        if self._client:
            await self._client.disconnect()
            logger.info("Отключено от Telegram")
    
    async def get_channel_messages(
        self,
        channel: str,
        min_id: Optional[int] = None,
        limit: int = 100
    ) -> List[Message]:
        """
        Получить сообщения из канала.
        
        Args:
            channel: Username канала (например, @eddytester)
            min_id: Получать сообщения с ID больше этого (для инкрементального обновления)
            limit: Максимальное количество сообщений
        
        Returns:
            Список сообщений
        """
        if not self._client:
            raise RuntimeError("Клиент не подключён")
        
        entity = await self._client.get_entity(channel)
        
        messages = []
        async for message in self._client.iter_messages(
            entity,
            min_id=min_id,
            limit=limit
        ):
            if message.text:  # Только сообщения с текстом
                messages.append(message)
        
        logger.info(f"Получено {len(messages)} сообщений из {channel}")
        return messages
    
    async def get_last_message_id(self, channel: str) -> Optional[int]:
        """Получить ID последнего сообщения в канале."""
        if not self._client:
            raise RuntimeError("Клиент не подключён")
        
        entity = await self._client.get_entity(channel)
        async for message in self._client.iter_messages(entity, limit=1):
            return message.id
        
        return None
