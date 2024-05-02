from aiogram import types, Router
import config

keyboard_router = Router()


@keyboard_router.callback_query(lambda c: c.data == "btnBan_id")
async def to_query(callback: types.callback_query):
    config.usersBan_id.append(callback.from_user.id)
    config.usersBan.append(f'@{callback.from_user.username}')
    await update_keyboard(callback.message)

    if len(config.usersBan_id) >= config.limit:
        await answer_final_keyboard(callback.message, True)
        await remove_candidate_keyboard()
        await remove_bot_keyboard()
        await remove_trigger_keyboard()
        await return_variables()


@keyboard_router.callback_query(lambda c: c.data == "btnFree_id")
async def to_query(callback: types.callback_query):
    config.usersFree_id.append(callback.from_user.id)
    config.usersFree.append(f'@{callback.from_user.username}')
    await update_keyboard(callback.message)

    if len(config.usersFree_id) >= config.limit:
        await answer_final_keyboard(callback.message, False)
        await remove_bot_keyboard()
        await return_variables()


def get_keyboard():
    button_ban = types.InlineKeyboardButton(
        text=f'Заблокировать {len(config.usersBan_id)}/{config.limit}',
        callback_data="btnBan_id")
    button_free = types.InlineKeyboardButton(
        text=f'Помиловать ✔  {len(config.usersFree_id)}/{config.limit}',
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
    return f'@{config.userTrigger} предложено заблокировать пользователя @{config.candidate}'


async def update_keyboard(message: types.Message):
    await message.edit_text(text=get_keyboard_text(),
                            reply_markup=get_keyboard()
                            )


async def remove_candidate_keyboard():
    await config.messageCandidate.delete()
    # TODO блокировка пользователя


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
    config.usersFree = []


async def answer_final_keyboard(message: types.Message, result: bool):
    if result:
        await message.answer(text=f'Пользователь @{config.candidate} заблокирован!\n'
                                  f'Проголосовшие: {", ".join(config.usersBan)}')
    else:
        await message.answer(text=f'Пользователь @{config.candidate} помилован!\n'
                                  f'Проголосовшие: {", ".join(config.usersFree)}')
