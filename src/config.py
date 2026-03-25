"""
Конфигурация приложения.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Загрузка .env файла
load_dotenv()


class Config:
    """Конфигурация приложения из переменных окружения."""
    
    # Telegram (теперь только бот)
    TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@eddytester")
    
    # AI
    AI_PROVIDER = os.getenv("AI_PROVIDER", "deepseek")
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")
    
    # Telegram бот
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID", "0"))
    
    # Расписание
    SCHEDULE_CRON = os.getenv("SCHEDULE_CRON", "0 0 */2 * *")
    
    # Логирование
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Пути
    BASE_DIR = Path(__file__).parent.parent
    DB_PATH = BASE_DIR / "automator.db"
    LOG_PATH = BASE_DIR / "logs" / "automator.log"
    
    @classmethod
    def validate(cls) -> list:
        """
        Проверка конфигурации.
        
        Returns:
            Список ошибок валидации
        """
        errors = []
        
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN не настроен")
        
        if cls.TELEGRAM_USER_ID == 0:
            errors.append("TELEGRAM_USER_ID не настроен")
        
        if not cls.AI_API_KEY:
            errors.append("AI_API_KEY не настроен")
        
        return errors
    
    @classmethod
    def print_config(cls):
        """Вывод конфигурации (без секретов)."""
        logging.info("=" * 40)
        logging.info("Конфигурация Automator:")
        logging.info(f"  Канал: {cls.TELEGRAM_CHANNEL}")
        logging.info(f"  AI провайдер: {cls.AI_PROVIDER}")
        logging.info(f"  AI модель: {cls.AI_MODEL}")
        logging.info(f"  Расписание: {cls.SCHEDULE_CRON}")
        logging.info(f"  User ID: {cls.TELEGRAM_USER_ID}")
        logging.info("=" * 40)
