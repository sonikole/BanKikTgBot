from aiogram import types, F, Router
from aiogram.filters import CommandStart

import config
from config import *
from handlers.keyboard import get_keyboard_text, get_keyboard

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(helpText)


@user_private_router.message()
async def get_text_messages(message: types.Message):
    if message.text == messageBan:
        global candidate
        global userTrigger
        global userTrigger_messageId
        global messageToBan

        try:
            candidate = message.reply_to_message.from_user.username
            userTrigger = message.from_user.username
            userTrigger_messageId = message.message_id
            messageToBan = get_keyboard_text()
            await message.answer(text=messageToBan,
                                 reply_markup=get_keyboard())
        except:
            await message.answer(text=f'@{message.from_user.username}\n{helpText}',
                                 parse_mode="Markdown")

    if message.text == "/help":
        await message.answer('/help — Показывает это сообщение\n'
                             '/limit — Изменить количество голосов для кика пользователя\n'
                             '/kickWord — Добавить слова для начала голосования. Попробуйте, например "/setKickWord кик"')
    elif message.text == "/limit":
        await message.answer(
            f'@{botName} теперь будет кикать пользователя, если {limit} людей проголосуют за это. Спасибо!')
    elif F.text is int:
        await message.answer("настройка limit")

