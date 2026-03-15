import asyncio
import logging
import socket
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Настройки
TOKEN = '8397466263:AAHtAa10rgS1dQAbi282PypGmvHduT5F60U'  # ТВОЙ ТОКЕН
LUA_SOCKET_PORT = 8888

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура (кнопки будут под сообщением)
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚪 Выйти"), KeyboardButton(text="💥 Крашнуть")]
    ],
    resize_keyboard=True,  # Автоматически подгоняет размер кнопок
    one_time_keyboard=False  # Кнопки остаются после нажатия
)

def send_to_lua(command):
    """Отправка команды в Lua скрипт через сокет"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', LUA_SOCKET_PORT))
        sock.send(json.dumps({'command': command}).encode())
        sock.close()
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот управления игрой Arizona RP\n"
        "Используй кнопки ниже для управления:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "🚪 Выйти")
async def exit_game(message: types.Message):
    if send_to_lua('exit'):
        await message.answer("✅ Команда 'Выйти' отправлена в игру")
    else:
        await message.answer("❌ Ошибка подключения к игре")

@dp.message(lambda message: message.text == "💥 Крашнуть")
async def crash_game(message: types.Message):
    if send_to_lua('crash'):
        await message.answer("✅ Команда 'Крашнуть' отправлена в игру")
    else:
        await message.answer("❌ Ошибка подключения к игре")

async def main():
    print("🤖 Бот запущен...")
    print("📱 Кнопки будут появляться под сообщением в Telegram")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
