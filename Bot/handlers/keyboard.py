from aiogram import types, Router
from Bot import config
from aiogram.methods import BanChatMember, UnbanChatMember
from threading import Timer
from datetime import datetime, timedelta
import time

keyboard_router = Router()


@keyboard_router.callback_query(lambda c: c.data == "btnBan_id")
async def to_query(callback: types.callback_query):
    config.usersBan.append(callback.from_user)
    config.usersBan_username.append(f'@{callback.from_user.username}')

    await update_keyboard(callback.message)

    if len(config.usersBan) >= config.limit:
        await answer_final_keyboard(callback.message, True)
        await remove_bot_keyboard()
        await remove_trigger_keyboard()
        # await ban_candidate(callback.message)  # удалить кандидата из группы
        # await unban_candidate(callback.message)  # дать возможность кандидату вернуться в группу

        await remove_candidate_keyboard(callback.message)  # удалить сообщение кандидата

        await return_variables()


@keyboard_router.callback_query(lambda c: c.data == "btnFree_id")
async def to_query(callback: types.callback_query):
    config.usersFree.append(callback.from_user)
    config.usersFree_username.append(f'@{callback.from_user.username}')
    await update_keyboard(callback.message)

    if len(config.usersFree) >= config.limit:
        await answer_final_keyboard(callback.message, False)
        await remove_bot_keyboard()
        await return_variables()


def get_keyboard():
    button_ban = types.InlineKeyboardButton(
        text=f'Заблокировать {len(config.usersBan)}/{config.limit}',
        callback_data="btnBan_id")
    button_free = types.InlineKeyboardButton(
        text=f'Помиловать ✔  {len(config.usersFree)}/{config.limit}',
        callback_data="btnFree_id")
    buttons = [
        [
            button_ban,
            button_free
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_text():
    return f'@{config.userTrigger} предложено заблокировать пользователя @{config.candidate.username}'


async def update_keyboard(message: types.Message):
    await message.edit_text(text=get_keyboard_text(),
                            reply_markup=get_keyboard()
                            )


async def remove_candidate_keyboard(message: types.Message):
    """
    Функция удаляет сообщение кандидата на блокировку
    """

    await config.messageCandidate.delete()


async def ban_candidate(message: types.Message):
    # TODO блокировка пользователя не забыть ВКЛЮЧИТЬ
    await message.bot(BanChatMember(chat_id=message.chat.id,
                                    user_id=config.candidate.id))
    # await send_temp_message(message)


async def unban_candidate(message: types.Message):
    # TODO блокировка пользователя не забыть ВКЛЮЧИТЬ
    await message.bot(UnbanChatMember(chat_id=message.chat.id,
                                      user_id=config.candidate.id))

    # await send_temp_message(message)


async def remove_bot_keyboard():
    await config.messageBot.delete()


async def remove_trigger_keyboard():
    await config.messageTrigger.delete()


async def return_variables():
    config.count_ban = 0
    config.count_free = 0
    config.candidate = None
    config.userTrigger = None
    config.usersBan = []
    config.usersFree_username = []


async def answer_final_keyboard(message: types.Message, result: bool):
    if result:
        await message.answer(text=f'Пользователь @{config.candidate.username} заблокирован!\n'
                                  f'Проголосовшие: {", ".join(config.usersBan_username)}')
    else:
        await message.answer(text=f'Пользователь @{config.candidate.username} помилован!\n'
                                  f'Проголосовшие: {", ".join(config.usersFree_username)}')


#TODO временное
async def send_temp_message(message: types.Message):
    s = 10
    i = 0

    def getTempMessageText():
        return 'Функция блокировка пользователя временно отключена\n' \
               f'Данное сообщение удалится через {s - i} секунд'

    messageTemp = await message.answer(text=getTempMessageText())

    while True:
        i += 1
        time.sleep(1)
        if i >= s:
            await messageTemp.delete()
            break
        else:
            await messageTemp.edit_text(text=getTempMessageText())
