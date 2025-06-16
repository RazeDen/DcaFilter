import asyncio
import sys
from bot.aiogram_handler import run_aiogram_polling, bot
from bot.telethon_handler import client


async def main():

    await client.start()
    print("✅ Код стартував")

    tasks = [
        asyncio.create_task(client.run_until_disconnected(), name="telethon"),
        asyncio.create_task(run_aiogram_polling(), name="aiogram"),
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    print("🔌 Вимикаємо клієнтів...")
    await client.disconnect()
    await bot.session.close()
    print("✅ Завершено!")

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())


