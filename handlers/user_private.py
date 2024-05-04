from aiogram import types, F, Router
from aiogram.filters import CommandStart
from handlers.keyboard import get_keyboard_text, get_keyboard
from aiogram.enums import ParseMode
import config

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(text=config.getStartText(),
                         parse_mode=ParseMode.HTML)


@user_private_router.message()
async def get_text_messages(message: types.Message):
    if message.text.lower() in config.textTrigger:
        config.candidate = message.reply_to_message.from_user.username
        config.messageCandidate = message.reply_to_message
        config.userTrigger = message.from_user.username
        config.usersBan.append('@' + config.userTrigger)
        config.usersBan_id.append(message.from_user.id)
        config.messageTrigger = message
        config.messageToBan = get_keyboard_text()
        config.messageBot = await message.answer(text=get_keyboard_text(),
                                                 reply_markup=get_keyboard())

    if message.text == "/help":
        await message.answer(text=config.getHelpText(),
                             parse_mode=ParseMode.HTML)

    elif message.text.startswith("/limit") and message.text != "/limit":
        text = message.text.split(" ", 1)[1]
        if text.isdigit():
            config.limit = int(text)
            await message.answer(text=config.getLimitText(),
                                 parse_mode=ParseMode.HTML)

    elif message.text.startswith("/addWord ") and message.text != "/addWord":
        text = message.text.split(" ", 1)[1].strip()

        if text in config.textTrigger:
            await message.answer(text=f'"{text}" уже присутствует в словаре\n\n'
                                      f'Текущие слова-триггеры: \n{", ".join(config.textTrigger)}',
                                 parse_mode=ParseMode.HTML)
        elif not (" " in text):
            config.textTrigger.append(text)
            await message.answer(text=config.getAddWordText(),
                                 parse_mode=ParseMode.HTML)

    elif message.text.startswith("/removeWord ") and message.text != "/removeWord":
        text = message.text.split(" ", 1)[1].strip()
        if not (" " in text):
            if text in config.textTrigger:
                config.textTrigger.remove(text)
                await message.answer(text=config.getRemoveWordText(),
                                     parse_mode=ParseMode.HTML)
            else:
                await message.answer(text=f'Слово "{text}" не найдено в словаре бота.\n\n'
                                          f'Текущие слова-триггеры: \n{", ".join(config.textTrigger)}',
                                     parse_mode=ParseMode.HTML)
