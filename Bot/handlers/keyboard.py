from aiogram import types, Router
from Bot import config

keyboard_router = Router()


@keyboard_router.callback_query(lambda c: c.data == "btnBan_id")
async def click_button_ban(callback: types.callback_query):
    """ Обработчик события.
    Нажание на кнопку "Заблокировать" """

    config.usersBan.append(callback.from_user)
    config.usersBan_username.append(f'@{callback.from_user.username}')

    await update_keyboard(callback.message)

    if len(config.usersBan) >= config.limit:
        await remove_bot_keyboard()

        await config.messageCandidate.delete()  # Удалить сообщение кандидата

        # TODO включить позже
        # await callback.message.bot(BanChatMember(chat_id=callback.message.chat.id,
        #                                          user_id=config.candidate.id))  # блокировка кандидата
        #
        # await callback.message.bot(UnbanChatMember(chat_id=callback.message.chat.id,
        #                                            user_id=config.candidate.id))  # дать возможность кандидату вернуться в группу

        await config.messageTrigger.delete()  # Удалить сообщение пользователя, запросившего блокировку

        await answer_final_keyboard(callback.message, True)
        await return_variables()


@keyboard_router.callback_query(lambda c: c.data == "btnFree_id")
async def click_button_free(callback: types.callback_query):
    """ Обработчик события.
    Нажание на кнопку "Помиловать" """

    config.usersFree.append(callback.from_user)
    config.usersFree_username.append(f'@{callback.from_user.username}')
    await update_keyboard(callback.message)

    if len(config.usersFree) >= config.limit:
        await answer_final_keyboard(callback.message, False)
        await remove_bot_keyboard()
        await return_variables()


def get_keyboard():
    """ Обновить сообщение бота """

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
    """ Сообщение бота.
    Ответ на триггер-слово """
    return f'@{config.userTrigger.username} предложено заблокировать пользователя @{config.candidate.username}'


async def update_keyboard(message: types.Message):
    """ Сообщение бота.
    Обновить ответ на триггер-слово """
    await message.edit_text(text=get_keyboard_text(),
                            reply_markup=get_keyboard())


async def remove_bot_keyboard():
    """ Сообщение бота.
    Удалить """
    await config.messageBot.delete()


async def remove_trigger_keyboard():
    """ Удалить триггер-сообщение """
    await config.messageTrigger.delete()


async def return_variables():
    """ Обнулить переменные для чата """
    config.count_ban = 0
    config.count_free = 0
    config.candidate = None
    config.userTrigger = None
    config.usersBan = []
    config.usersFree_username = []


async def answer_final_keyboard(message: types.Message, result: bool):
    """ Результат голосования """
    if result:
        await message.answer(text=f'Пользователь @{config.candidate.username} заблокирован!\n'
                                  f'Проголосовшие: {", ".join(config.usersBan_username)}')
    else:
        await message.answer(text=f'Пользователь @{config.candidate.username} помилован!\n'
                                  f'Проголосовшие: {", ".join(config.usersFree_username)}')
