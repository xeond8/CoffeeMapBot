from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.lexicon_eng import LEXICON_ENG
from lexicon.lexicon_ru import LEXICON_RU


def send_geolocation_keyboard(lang_code: str) -> ReplyKeyboardMarkup:
    if lang_code == 'ru':
        geo_button: KeyboardButton = KeyboardButton(text=LEXICON_RU['Send Geo'], request_location=True)
    else:
        geo_button: KeyboardButton = KeyboardButton(text=LEXICON_ENG['Send Geo'], request_location=True)
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(geo_button)
    return keyboard
