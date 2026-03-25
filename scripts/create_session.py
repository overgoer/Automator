#!/usr/bin/env python3
"""
Скрипт для создания Telegram сессии.
Запустите один раз для авторизации второго аккаунта.
"""

import os
import sys
import asyncio
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()


async def create_session():
    """Создание сессии Telegram."""
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    
    if not api_id or not api_hash:
        print("❌ TELEGRAM_API_ID и TELEGRAM_API_HASH должны быть в .env")
        print("   Получите их на https://my.telegram.org/apps")
        sys.exit(1)
    
    session_path = "./src/automator_session"
    
    print("📱 Создание сессии Telegram...")
    print("   Введите номер телефона второго аккаунта")
    print("   Код подтверждения придёт в Telegram\n")
    
    client = TelegramClient(session_path, int(api_id), api_hash)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        phone = input("Введите номер телефона (с +7): ")
        await client.send_code_request(phone)
        
        code = input("Введите код из Telegram: ")
        
        try:
            await client.sign_in(phone, code)
            print("\n✅ Авторизация успешна!")
            print(f"📁 Сессия сохранена: {os.path.abspath(session_path)}.*")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            sys.exit(1)
    else:
        print("✅ Клиент уже авторизован")
    
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(create_session())
