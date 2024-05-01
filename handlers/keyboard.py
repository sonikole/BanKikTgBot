from aiogram import types, Router

import config
from config import *

keyboard_router = Router()


@keyboard_router.callback_query(lambda c: c.data == "btnBanTrue_id")
async def to_query(callback: types.callback_query):
    config.count_ban += 1
    await update_keyboard(callback.message)

    if config.count_ban > limit:
        await remove_keyboard(callback.message)
        await remove_trigger(callback.message)


def get_keyboard():
    button_ban = types.InlineKeyboardButton(
        text=f'Заблокировать {count_ban}/{limit}',
        callback_data="btnBanTrue_id")
    button_free = types.InlineKeyboardButton(
        text=f'Помиловать ✔️ {count_free}/{limit}',
        callback_data="btnBanFalse_id")
    buttons = [
        [
            button_ban,
            button_free
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_text():
    return f'@{userTrigger} предложено заблокировать пользователя @{candidate}'


async def update_keyboard(message: types.Message):
    await message.edit_text(text=messageToBan,
                            reply_markup=get_keyboard()
                            )


async def remove_keyboard(message: types.Message):
    await message.delete()


async def remove_trigger(message: types.Message):
    await message.from_user.delete()
