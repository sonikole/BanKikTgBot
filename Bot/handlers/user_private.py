from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from Bot.handlers.keyboard import get_keyboard_text, get_keyboard
from Bot import config

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text=config.getStartText(),
                         parse_mode=ParseMode.HTML)


@user_private_router.message()
async def get_text_messages(message: types.Message):
    config.chat = message.chat
    """Слова-триггеры
    /ban
    /help
    /limit
    /addWord
    /removeWord
    """

    if message.text.lower() in config.textTrigger:
        await click_ban(message)

    elif message.text == "/help":
        await click_help(message)

    elif message.text.startswith("/limit") and message.text != "/limit":
        await click_limit(message)

    elif message.text.startswith("/addWord ") and message.text != "/addWord":
        await click_add_word(message)

    elif message.text.startswith("/removeWord ") and message.text != "/removeWord":
        await click_remove_word(message)


async def is_admin(message: types.Message, user: types.User) -> bool:
    admins = await message.bot.get_chat_administrators(chat_id=config.chat.id)
    admins_id = []

    for admin in admins:
        admins_id.append(admin.user.id)

    print(user.id in admins_id)

    return user.id in admins_id

async def is_self_ban():
    return config.candidate.id == config.userTrigger.id

async def click_ban(message: types.Message):
    config.candidate = message.reply_to_message.from_user
    config.userTrigger = message.from_user

    if await is_self_ban():
        print("самобан запрещен")
        pass
    elif await is_admin(message, config.candidate):
        print("блок админа")
        await message.answer(text=f'Пользователя @{config.candidate.username} нельзя предать правосудию',
                             parse_mode=ParseMode.HTML)
    else:
        print("блок не админа")
        config.messageCandidate = message.reply_to_message
        config.userTrigger = message.from_user
        config.usersBan.append(message.from_user)
        config.messageTrigger = message
        config.messageToBan = get_keyboard_text()
        config.messageBot = await message.answer(text=get_keyboard_text(),
                                                 reply_markup=get_keyboard())


async def click_help(message: types.Message):
    await message.answer(text=config.getHelpText(),
                         parse_mode=ParseMode.HTML)


async def click_limit(message):
    text = message.text.split(" ", 1)[1].strip()
    if text.isdigit():
        config.limit = int(text)
        await message.answer(text=config.getLimitText(),
                             parse_mode=ParseMode.HTML)


async def click_add_word(message):
    text = message.text.split(" ", 1)[1].strip()
    if text in config.textTrigger:
        await message.answer(text=f'"{text}" уже присутствует в словаре\n\n'
                                  f'Текущие слова-триггеры: \n{", ".join(config.textTrigger)}',
                             parse_mode=ParseMode.HTML)
    elif not (" " in text):
        config.textTrigger.append(text)
        await message.answer(text=config.getAddWordText(),
                             parse_mode=ParseMode.HTML)


async def click_remove_word(message):
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
