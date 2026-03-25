"""
Главный скрипт Automator.
Оркестрация всех компонентов.
"""

import asyncio
import logging
from datetime import datetime

from .config import Config
from .db.repository import Database
from .telegram.client import TelegramClientWrapper
from .telegram.scraper import PostScraper
from .ai.client import DeepSeekClient
from .ai.prompt import PromptManager
from .notifier.telegram_bot import TelegramNotifier


# Настройка логирования
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Config.LOG_PATH),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class Automator:
    """Основной класс приложения."""
    
    def __init__(self):
        self.db = Database(str(Config.DB_PATH))
        self.tg_client = TelegramClientWrapper(
            Config.TELEGRAM_API_ID,
            Config.TELEGRAM_API_HASH
        )
        self.scraper = PostScraper(self.tg_client, Config.TELEGRAM_CHANNEL)
        self.ai_client = DeepSeekClient(Config.AI_API_KEY, Config.AI_MODEL)
        self.notifier = TelegramNotifier(
            Config.TELEGRAM_BOT_TOKEN,
            Config.TELEGRAM_USER_ID
        )
        self.prompt_manager = PromptManager()
    
    async def initialize(self):
        """Инициализация всех компонентов."""
        logger.info("Инициализация Automator...")
        
        await self.db.init()
        await self.tg_client.connect()
        await self.ai_client.connect()
        await self.notifier.connect()
        
        logger.info("Все компоненты инициализированы")
    
    async def shutdown(self):
        """Корректное завершение работы."""
        logger.info("Завершение работы...")
        
        await self.tg_client.disconnect()
        await self.ai_client.close()
        await self.notifier.close()
        
        logger.info("Работа завершена")
    
    async def run(self):
        """
        Основной цикл работы.
        1. Получить новые посты из канала
        2. Сохранить в БД
        3. Отправить в ИИ для генерации
        4. Отправить результат пользователю
        """
        logger.info("Запуск цикла обработки...")
        
        try:
            # Получаем ID последнего обработанного сообщения
            last_processed_id = await self.db.get_last_processed_message_id()
            if last_processed_id is None:
                last_processed_id = 0
            
            logger.info(f"Последний обработанный message_id: {last_processed_id}")
            
            # Получаем новые посты
            new_posts = await self.scraper.fetch_new_posts(last_processed_id)
            
            if not new_posts:
                logger.info("Нет новых постов")
                await self.notifier.send_status("Нет новых постов для обработки")
                return
            
            logger.info(f"Найдено {len(new_posts)} новых постов")
            
            # Сохраняем посты в БД
            saved_post_ids = []
            for msg_id, text, date in new_posts:
                post_id = await self.db.save_post(msg_id, text, date)
                saved_post_ids.append((post_id, msg_id, text, date))
            
            # Генерируем контент на основе всех новых постов
            posts_for_prompt = [(msg_id, text, date) for _, msg_id, text, date in saved_post_ids]
            prompt = self.prompt_manager.get_generation_prompt(posts_for_prompt)
            
            logger.info("Генерация контента через ИИ...")
            generated_content = await self.ai_client.generate(
                system_prompt="Ты — опытный контент-мейкер для Telegram канала о тестировании QA.",
                user_prompt=prompt
            )
            
            # Сохраняем сгенерированный контент
            for post_id, _, _, _ in saved_post_ids:
                await self.db.save_generated_content(
                    post_id=post_id,
                    content=generated_content,
                    model=Config.AI_MODEL,
                    prompt=prompt
                )
                await self.db.mark_post_processed(post_id)
            
            logger.info(f"Контент сгенерирован: {len(generated_content)} символов")
            
            # Отправляем пользователю
            await self.notifier.send_post(generated_content)
            
            logger.info("Цикл обработки завершён успешно")
            
        except Exception as e:
            logger.exception(f"Ошибка в цикле обработки: {e}")
            await self.notifier.send_error(str(e))
            raise


async def main():
    """Точка входа."""
    Config.print_config()
    
    # Валидация конфигурации
    errors = Config.validate()
    if errors:
        for error in errors:
            logger.error(f"Ошибка конфигурации: {error}")
        return
    
    automator = Automator()
    
    try:
        await automator.initialize()
        await automator.run()
    finally:
        await automator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
