from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup

from keyboards.user_keyboards import send_geolocation_keyboard
from lexicon.lexicon_eng import LEXICON_ENG
from lexicon.lexicon_ru import LEXICON_RU
from services.db_functions import print_entry, find_three_nearest


async def send_geolocation(message: Message):
    lang_code: str = message.from_user.language_code
    kb: ReplyKeyboardMarkup = send_geolocation_keyboard(lang_code)
    if lang_code == 'ru':
        ans = LEXICON_RU['start']
    else:
        ans = LEXICON_ENG['start']
    await message.answer(ans, reply_markup=kb)


async def print_three_nearest(message: Message):
    lat_user: float = message.location.latitude
    lon_user: float = message.location.longitude
    print(lat_user, lon_user, message.from_user.username)
    lg_code: str = message.from_user.language_code
    nearest_shops = await find_three_nearest(lat_user, lon_user)
    for shop in nearest_shops:
        caption, photo_id = print_entry(shop, lg_code)
        await message.answer_photo(photo_id, caption=caption)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_geolocation, commands='start')
    dp.register_message_handler(print_three_nearest, content_types='location')
