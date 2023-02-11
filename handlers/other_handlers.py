from aiogram.types import Message
from aiogram import Dispatcher
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.lexicon_eng import LEXICON_ENG


async def other_handler(message: Message):
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['other'])
    else:
        await message.answer(LEXICON_ENG['other'])


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(other_handler)
