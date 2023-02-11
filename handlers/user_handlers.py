from keyboards.user_keyboards import send_geolocation_keyboard
from aiogram.types import Message
from aiogram import Dispatcher
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.lexicon_eng import LEXICON_ENG
from aiogram.types import ReplyKeyboardMarkup


async def start_handler(message: Message):
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['start'])
    else:
        await message.answer(LEXICON_ENG['start'])


async def send_geolocation(message: Message):
    lang_code: str = message.from_user.language_code
    kb: ReplyKeyboardMarkup = send_geolocation_keyboard(lang_code)
    if lang_code == 'ru':
        ans = LEXICON_RU['start']
    else:
        ans = LEXICON_ENG['start']
    await message.answer(ans, reply_markup=kb)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_geolocation, commands='start')