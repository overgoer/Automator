"""
Модели базы данных.
SQLite для хранения постов и сгенерированного контента.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    """Пост из Telegram канала."""
    id: int
    message_id: int
    text: str
    date: datetime
    processed: bool = False
    created_at: Optional[datetime] = None


@dataclass
class GeneratedContent:
    """Сгенерированный ИИ контент."""
    id: int
    post_id: int
    content: str
    model: str
    prompt: str
    created_at: datetime


@dataclass
class Config:
    """Конфигурация приложения."""
    key: str
    value: str
    updated_at: datetime
