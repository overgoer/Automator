"""
CRUD операции для базы данных.
"""

import aiosqlite
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from .models import Post, GeneratedContent, Config


class Database:
    """Управление базой данных SQLite."""
    
    def __init__(self, db_path: str = "automator.db"):
        self.db_path = Path(db_path)
    
    async def init(self):
        """Инициализация таблиц."""
        async with aiosqlite.connect(self.db_path) as db:
            # Таблица постов
            await db.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER UNIQUE NOT NULL,
                    text TEXT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    processed INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица сгенерированного контента
            await db.execute("""
                CREATE TABLE IF NOT EXISTS generated_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES posts(id)
                )
            """)
            
            # Таблица конфигурации
            await db.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()
    
    async def save_post(self, message_id: int, text: str, date: datetime) -> int:
        """Сохранить пост. Возвращает id поста."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT OR IGNORE INTO posts (message_id, text, date) VALUES (?, ?, ?)",
                (message_id, text, date)
            )
            await db.commit()
            return cursor.lastrowid or 0
    
    async def get_unprocessed_posts(self) -> List[Post]:
        """Получить все необработанные посты."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM posts WHERE processed = 0 ORDER BY date ASC"
            )
            rows = await cursor.fetchall()
            return [
                Post(
                    id=row["id"],
                    message_id=row["message_id"],
                    text=row["text"],
                    date=datetime.fromisoformat(row["date"]),
                    processed=bool(row["processed"]),
                    created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None
                )
                for row in rows
            ]
    
    async def mark_post_processed(self, post_id: int):
        """Отметить пост как обработанный."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE posts SET processed = 1 WHERE id = ?",
                (post_id,)
            )
            await db.commit()
    
    async def save_generated_content(
        self, post_id: int, content: str, model: str, prompt: str
    ) -> int:
        """Сохранить сгенерированный контент."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO generated_content (post_id, content, model, prompt) VALUES (?, ?, ?, ?)",
                (post_id, content, model, prompt)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_config(self, key: str) -> Optional[str]:
        """Получить значение конфигурации."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT value FROM config WHERE key = ?", (key,)
            )
            row = await cursor.fetchone()
            return row["value"] if row else None
    
    async def set_config(self, key: str, value: str):
        """Установить значение конфигурации."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO config (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (key, value)
            )
            await db.commit()
    
    async def get_last_processed_message_id(self) -> Optional[int]:
        """Получить ID последнего обработанного сообщения."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT message_id FROM posts WHERE processed = 1 ORDER BY date DESC LIMIT 1"
            )
            row = await cursor.fetchone()
            return row[0] if row else None
