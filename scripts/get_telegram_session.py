#!/usr/bin/env python3
"""
Скрипт для получения сессии Telegram (второй аккаунт).
Запросит номер телефона и код из Telegram, сохранит сессию.
"""

import os
import sys
from getpass import getpass

try:
    from telethon.sync import TelegramClient
except ImportError:
    print("❌ Telethon не установлен. Выполните: pip install telethon")
    sys.exit(1)

# Временные значения (будут заменены на реальные после ввода)
API_ID = input("Введите API_ID (с my.telegram.org): ").strip()
API_HASH = input("Введите API_HASH (с my.telegram.org): ").strip()

if not API_ID or not API_HASH:
    print("❌ API_ID и API_HASH обязательны")
    sys.exit(1)

PHONE = input("Введите номер второго аккаунта (например: +79991234567): ").strip()

SESSION_PATH = "./telegram_session"

print(f"\n📱 Начинаем авторизацию для {PHONE}...")
print("Код придёт в Telegram (второй аккаунт)\n")

client = TelegramClient(SESSION_PATH, int(API_ID), API_HASH)

with client:
    # Отправка кода
    client.send_code_request(PHONE)
    
    # Ввод кода
    code = input("Введите код из Telegram: ").strip()
    
    try:
        client.sign_in(PHONE, code)
        print("\n✅ Авторизация успешна!")
        print(f"📁 Сессия сохранена: {os.path.abspath(SESSION_PATH)}.*")
        print("\nТеперь приложение может использовать эту сессию для чтения канала.")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
