from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from Bot.handlers.keyboard import get_keyboard_text, get_keyboard
from Bot import config
from aiogram.types import Message, User
from aiogram.filters import Command

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_handler(message: Message):
    """ Реакция бота на /start """
    await message.answer(text=config.get_start_text(),
                         parse_mode=ParseMode.HTML)


@user_private_router.message(Command(commands='help'))
async def help_handler(message: Message):
    """ Реакция бота на /help """
    await message.answer(text=config.get_help_text(),
                         parse_mode=ParseMode.HTML)


@user_private_router.message(Command(commands='limit'))
async def limit_handler(message: Message):
    # rule = re.compile(r'^limit (\d+)$')
    try:
        """ Реакция бота на /limit """
        text = message.text.split(" ", 1)[1].strip()
        if text.isdigit():
            config.limit = int(text)
            await message.answer(text=config.get_limit_text(),
                                 parse_mode=ParseMode.HTML)

    except IndexError:
        print('ERROR /limit')


@user_private_router.message(Command(commands='addWord'))
async def add_word_handler(message: Message):
    """ Реакция бота на /addWord """
    try:
        text = message.text.split(" ", 1)[1].strip()
        if text in config.words_for_ban:
            await message.answer(text=f'"{text}" уже присутствует в словаре\n\n'
                                      f'Текущие слова-триггеры: \n{", ".join(config.words_for_ban)}',
                                 parse_mode=ParseMode.HTML)
        elif not (" " in text):
            config.words_for_ban.append(text)
            await message.answer(text=config.get_add_word_text(),
                                 parse_mode=ParseMode.HTML)
    except IndexError:
        print('ERROR /addWord')


@user_private_router.message(Command(commands='removeWord'))
async def remove_word_handler(message: Message):
    """ Реакция бота на /removeWord """
    try:

        text = message.text.split(" ", 1)[1].strip()
        if not (" " in text):
            if text in config.words_for_ban:
                config.words_for_ban.remove(text)
                await message.answer(text=config.get_remove_word_text(),
                                     parse_mode=ParseMode.HTML)
            else:
                await message.answer(text=f'Слово "{text}" не найдено в словаре бота.\n\n'
                                          f'Текущие слова-триггеры: \n{", ".join(config.words_for_ban)}',
                                     parse_mode=ParseMode.HTML)
    except IndexError:
        print('ERROR /removeWord')


@user_private_router.message()
async def ban_handler(message: Message):
    """ Реакция бота на /ban """
    config.chat = message.chat
    print("бан тест")
    if message.text in config.words_for_ban:
        print("слово в словаре")
        config.candidate = message.reply_to_message.from_user
        config.userTrigger = message.from_user

        if await is_self_ban():
            print("самобан запрещен")
            pass
        elif await is_admin(message, config.candidate):
            print("попытка блокировки админа")
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


# @user_private_router.message()
# async def message_handler(message: Message):
#     config.chat = message.chat
#
#     if message.text.lower() in config.words_for_ban:
#         await click_ban(message)


async def is_admin(message: Message, user: User) -> bool:
    admins = await message.bot.get_chat_administrators(chat_id=config.chat.id)
    admins_id = []

    for admin in admins:
        admins_id.append(admin.user.id)

    print(user.id in admins_id)

    return user.id in admins_id


async def is_self_ban():
    return config.candidate.id == config.userTrigger.id


# async def click_ban(message: Message):
#     """ Реакция бота на /ban """
#     config.candidate = message.reply_to_message.from_user
#     config.userTrigger = message.from_user
#
#     if await is_self_ban():
#         print("самобан запрещен")
#         pass
#     elif await is_admin(message, config.candidate):
#         print("попытка блокировки админа")
#         await message.answer(text=f'Пользователя @{config.candidate.username} нельзя предать правосудию',
#                              parse_mode=ParseMode.HTML)
#     else:
#         print("блок не админа")
#         config.messageCandidate = message.reply_to_message
#         config.userTrigger = message.from_user
#         config.usersBan.append(message.from_user)
#         config.messageTrigger = message
#         config.messageToBan = get_keyboard_text()
#         config.messageBot = await message.answer(text=get_keyboard_text(),
#                                                  reply_markup=get_keyboard())
