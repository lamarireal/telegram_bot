from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.router import Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import F
import os
from binanceAPI import get_balance, get_client_binance, get_price, get_important_coin
from dotenv import load_dotenv

# Токен Telegram-бота
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Создание объектов
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/wallet"), KeyboardButton(text="/help")],
        [KeyboardButton(text="/items"), KeyboardButton(text="/price BTCUSDT")],
    ],
    resize_keyboard=True  
)

# Создание Binance клиента
client = get_client_binance()



async def send_welcome(message: Message):
    balance = get_balance(client)
    await message.answer(f"Balance USDT: {balance['free']}", reply_markup=keyboard)



async def send_help(message: Message):
    help_text = (
        "This bot is designed to help you manage your Binance account and track cryptocurrency data.\n\n"
        "Available commands:\n"
        "/wallet - View your Binance wallet balance\n"
        "/help - Display this help message with available commands\n"
        "/items - View the most important coins\n"
        "/price <coin_pair> - Check the current price of a specific coin (e.g., /price BTCUSDT)\n"
    )
    await message.answer(help_text, reply_markup=keyboard)

async def send_price(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("please, choose coin", reply_markup=keyboard)
        return

    symbol = parts[1].upper()
    price = get_price(client, symbol)

    print(symbol, price)

    if isinstance(price, float):
        await message.answer(f"Текущая цена {symbol}: {price} USDT", reply_markup=keyboard)
    else:
        await message.answer(price, reply_markup=keyboard)



async def send_important_coin(message: Message):
    results = get_important_coin(client)

    if isinstance(results, str):
        await message.answer(results)
        return

    response = "\n".join([f"{coin}: {price} USDT" for coin, price in results.items()])
    await message.answer("List of coins:")
    await message.answer(response, reply_markup=keyboard)






def register_handlers():
    router.message.register(send_welcome, F.text == "/wallet")
    router.message.register(send_help, F.text == "/help")
    router.message.register(send_price, F.text.startswith("/price"))
    router.message.register(send_important_coin, F.text == "/items")



async def start_bot():
    register_handlers()
    await dp.start_polling(bot)
