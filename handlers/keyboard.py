from aiogram import types, Router
import config

keyboard_router = Router()


@keyboard_router.callback_query(lambda c: c.data == "btnBanTrue_id")
async def to_query(callback: types.callback_query):
    config.count_ban += 1
    await update_keyboard(callback.message)

    if config.count_ban >= config.limit:
        await remove_keyboard()


def get_keyboard():
    button_ban = types.InlineKeyboardButton(
        text=f'Заблокировать {config.count_ban}/{config.limit}',
        callback_data="btnBanTrue_id")
    button_free = types.InlineKeyboardButton(
        text=f'Помиловать ✔️ {config.count_free}/{config.limit}',
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
    return f'@{config.userTrigger} предложено заблокировать пользователя @{config.candidate}'


async def update_keyboard(message: types.Message):
    await message.edit_text(text=get_keyboard_text(),
                            reply_markup=get_keyboard()
                            )


async def remove_keyboard():
    await config.messageBot.delete()
    await config.messageTrigger.delete()
    await config.messageCandidate.delete()
    config.count_ban = 0
    config.count_free = 0
    config.candidate = None
    config.userTrigger = None
    config.usersBan = []
    config.usersFree = []
