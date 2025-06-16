import asyncio
from aiogram import Bot, Dispatcher
from config import api_token

bot = Bot(token=api_token)
dp = Dispatcher()

async def run_aiogram_polling():
    await dp.start_polling(bot)


