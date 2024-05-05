import asyncio
from aiogram import Bot, Dispatcher
from config import *
from Bot.handlers.keyboard import keyboard_router
from Bot.handlers.user_private import user_private_router

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_routers(user_private_router, keyboard_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, alloved_updates=ALLOWED_UPDATES)


# TODO: Кандидат не должен участвовать в голосовании. (сделать так, чтобы его кнопка не зависала)
# TODO: Таймаут у бота. Проверка, что такого сообщения не было
# TODO: Пользователь может убрать свой голос (но тогда список проголосовавших показывать сразу)
# TODO: Работа на два чата
# TODO: Добавить настройку "Кик, бан, разрешить только просмотр"
# TODO: Реализовать для кандидата "разрешить только просмотр"

asyncio.run(main())
