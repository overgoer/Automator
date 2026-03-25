"""
Telegram бот для отправки уведомлений пользователю.
"""

import logging
from aiogram import Bot
from aiogram.enums import ParseMode

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Отправка уведомлений через Telegram бота."""
    
    def __init__(self, bot_token: str, user_id: int):
        self.bot_token = bot_token
        self.user_id = user_id
        self._bot = None
    
    async def connect(self):
        """Инициализация бота."""
        self._bot = Bot(token=self.bot_token)
        
        # Проверка подключения
        me = await self._bot.get_me()
        logger.info(f"Бот @{me.username} инициализирован")
    
    async def close(self):
        """Закрытие бота."""
        if self._bot:
            await self._bot.session.close()
            logger.info("Бот закрыт")
    
    async def send_message(self, text: str, parse_mode: str = ParseMode.MARKDOWN):
        """
        Отправить сообщение пользователю.
        
        Args:
            text: Текст сообщения
            parse_mode: Режим парсинга (Markdown, HTML, etc.)
        """
        if not self._bot:
            raise RuntimeError("Бот не инициализирован")
        
        try:
            await self._bot.send_message(
                chat_id=self.user_id,
                text=text,
                parse_mode=parse_mode
            )
            logger.info(f"Сообщение отправлено пользователю {self.user_id}")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            raise
    
    async def send_post(self, post_text: str):
        """
        Отправить готовый пост пользователю.
        
        Args:
            post_text: Текст поста (с форматированием)
        """
        # Добавляем преамбулу
        message = (
            "🤘 <b>Новый пост готов!</b>\n\n"
            f"{post_text}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ Готово к публикации в @eddytester"
        )
        
        await self.send_message(message, parse_mode=ParseMode.HTML)
    
    async def send_error(self, error_text: str):
        """
        Отправить сообщение об ошибке.
        
        Args:
            error_text: Текст ошибки
        """
        message = (
            "❌ <b>Ошибка в Automator</b>\n\n"
            f"<code>{error_text}</code>\n\n"
            "Проверь логи для деталей."
        )
        
        await self.send_message(message, parse_mode=ParseMode.HTML)
    
    async def send_status(self, status_text: str):
        """
        Отправить статус выполнения.
        
        Args:
            status_text: Текст статуса
        """
        message = f"✅ <b>Automator</b>\n\n{status_text}"
        await self.send_message(message, parse_mode=ParseMode.HTML)
