from aiogram import types, F, Router
from aiogram.filters import CommandStart

import config
from handlers.keyboard import get_keyboard_text, get_keyboard

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(config.helpText)


@user_private_router.message()
async def get_text_messages(message: types.Message):
    if message.text == config.messageBan:
        try:
            config.candidate = message.reply_to_message.from_user.username
            config.messageCandidate = message.reply_to_message
            config.userTrigger = message.from_user.username
            config.messageTrigger = message
            config.messageToBan = get_keyboard_text()
            config.messageBot = await message.answer(text=config.messageToBan,
                                                     reply_markup=get_keyboard())

        except:
            await message.answer(text=f'@{message.from_user.username}\n{config.helpText}',
                                 parse_mode="Markdown")

    if message.text == "/help":
        await message.answer('/help — Показывает это сообщение\n'
                             '/limit — Изменить количество голосов для кика пользователя\n'
                             '/kickWord — Добавить слова для начала голосования. Попробуйте, например "/setKickWord кик"')
    elif message.text.startswith("/limit"):
        text = message.text.split(" ", 1)[1]
        if text.isdigit():
            config.limit = int(text)
            await message.answer(
                f'Теперь лимит голосующих = {config.limit}.')
    elif F.text is int:
        await message.answer("настройка limit")
