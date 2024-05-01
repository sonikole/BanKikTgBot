from aiogram import types, F, Router
from aiogram.filters import CommandStart
from handlers.keyboard import get_keyboard_text, get_keyboard
import config

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(config.helpText)


@user_private_router.message()
async def get_text_messages(message: types.Message):
    if message.text.lower() in config.textTrigger:
        try:
            config.candidate = message.reply_to_message.from_user.username
            config.messageCandidate = message.reply_to_message
            config.userTrigger = message.from_user.username
            config.messageTrigger = message
            config.messageToBan = get_keyboard_text()
            config.messageBot = await message.answer(text=get_keyboard_text(),
                                                     reply_markup=get_keyboard())

        except:
            await message.answer(text=f'@{message.from_user.username}\n{config.helpText}',
                                 parse_mode="Markdown")

    if message.text == "/help":
        await message.answer('/help — Показывает это сообщение\n'
                             '/limit — Изменить количество голосов для кика пользователя\n'
                             '/kickWord — Добавить слова для начала голосования. Попробуйте, например "/setKickWord кик"')
    elif message.text.startswith("/limit"):
        if message.text != "/limit":
            text = message.text.split(" ", 1)[1]
            if text.isdigit():
                config.limit = int(text)
                await message.answer(
                    f'Теперь лимит голосующих = {config.limit}.')

    elif message.text.startswith("/kickWord"):
        text = message.text.split(" ", 1)[1].strip()
        if False == " " in text:
            config.textTrigger.append(text)
            await message.answer(
                f'Теперь затриггерить @{config.botName} можно с момощью слов:\n{config.limit}.')
