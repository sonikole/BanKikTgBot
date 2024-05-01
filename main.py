import asyncio
from aiogram import Bot, Dispatcher
from config import *
from handlers.keyboard import keyboard_router
from handlers.user_private import user_private_router

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_routers(user_private_router, keyboard_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, alloved_updates=ALLOWED_UPDATES)


asyncio.run(main())
