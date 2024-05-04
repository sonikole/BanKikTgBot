from unittest.mock import AsyncMock
import pytest
from aiogram.enums import ParseMode

from Bot import config
from Bot.handlers.user_private import start


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await start(message)

    message.answer.assert_called_with(text=config.getStartText(),
                                      parse_mode=ParseMode.HTML)
    message.answer.assert_called_with(text='dgfhfh',
                                      parse_mode=ParseMode.HTML)
