from aiogram import types, F, Router
from aiogram.filters import CommandStart
from handlers.keyboard import get_keyboard_text, get_keyboard
from aiogram.enums import ParseMode
import config

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(text=config.helpText,
                         parse_mode=ParseMode.HTML)


@user_private_router.message()
async def get_text_messages(message: types.Message):
    if message.text.lower() in config.textTrigger:
        try:
            config.candidate = message.reply_to_message.from_user.username
            config.messageCandidate = message.reply_to_message
            config.userTrigger = message.from_user.username
            config.usersBan.append(config.userTrigger)
            config.usersBan_id.append(message.from_user.id)
            config.messageTrigger = message
            config.messageToBan = get_keyboard_text()
            config.messageBot = await message.answer(text=get_keyboard_text(),
                                                     reply_markup=get_keyboard())
        except:
            await message.answer(text=f'@{message.from_user.username}\n{config.helpText}',
                                 parse_mode="Markdown")

    if message.text == "/help":
        await message.answer(text='/help — Показывает это сообщение\n'
                                  '/limit — Изменить количество голосов для кика пользователя\n'
                                  '/addKikWord — Добавить слова-триггеры для начала голосования. Попробуйте например <b>"/addKikWord кик"</b>\n\n'
                                  f'Текущие слова-триггеры: \n{", ".join(config.textTrigger)}',
                             parse_mode=ParseMode.HTML)

    elif message.text.startswith("/limit"):
        if message.text != "/limit":
            text = message.text.split(" ", 1)[1]
            if text.isdigit():
                config.limit = int(text)
                await message.answer(
                    f'Теперь лимит голосующих = {config.limit}.')

    elif message.text.startswith("/addKikWord"):
        if message.text != "/addKikWord":
            text = message.text.split(" ", 1)[1].strip()
            if not (" " in text):
                config.textTrigger.append(text)
                await message.answer(text=f'Теперь затриггерить @{config.botName} можно с помощью слов:\n'
                                          f'<b>{", ".join(config.textTrigger)}</b>.',
                                     parse_mode=ParseMode.HTML)
