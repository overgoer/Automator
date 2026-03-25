"""
AI клиент для работы с DeepSeek API.
"""

import logging
from typing import Optional
import httpx

logger = logging.getLogger(__name__)


class DeepSeekClient:
    """Клиент для DeepSeek API."""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com"
        self._client: Optional[httpx.AsyncClient] = None
    
    async def connect(self):
        """Инициализация HTTP клиента."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )
        logger.info("DeepSeek клиент инициализирован")
    
    async def close(self):
        """Закрытие HTTP клиента."""
        if self._client:
            await self._client.aclose()
            logger.info("DeepSeek клиент закрыт")
    
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000
    ) -> str:
        """
        Генерация ответа от ИИ.
        
        Args:
            system_prompt: Системный промпт (роль, контекст)
            user_prompt: Пользовательский промпт (задача)
            max_tokens: Максимальное количество токенов в ответе
        
        Returns:
            Сгенерированный текст
        """
        if not self._client:
            raise RuntimeError("Клиент не инициализирован")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self._client.post(
                "/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                }
            )
            response.raise_for_status()
            data = response.json()
            
            content = data["choices"][0]["message"]["content"]
            logger.info(f"Генерация завершена: {len(content)} символов")
            return content
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP ошибка при генерации: {e}")
            raise
        except KeyError as e:
            logger.error(f"Неверный формат ответа от API: {e}")
            raise RuntimeError(f"Ошибка парсинга ответа API: {e}")
    
    async def test_connection(self) -> bool:
        """Проверка подключения к API."""
        try:
            await self.generate(
                system_prompt="Ты тестовый ассистент.",
                user_prompt="Ответь 'OK' одним словом.",
                max_tokens=10
            )
            return True
        except Exception as e:
            logger.error(f"Тест подключения не удался: {e}")
            return False
